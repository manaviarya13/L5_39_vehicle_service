"""Vehicle service management demo used for Lab 5 static analysis."""

import hashlib
import json
import logging
import shutil
from datetime import date
from pathlib import Path

SERVICE_RATES = {
    "Oil Change": 1500,
    "Wheel Alignment": 800,
    "General": 2500,
    "Brake Check": 1200,
}
service_records = {}
LOGGER = logging.getLogger(__name__)


def add_service(vehicle_no, service_type="General", history=None):
    """Add a service record and return a call-specific history list."""
    if not isinstance(vehicle_no, str) or not vehicle_no.strip():
        raise ValueError("vehicle_no must be a non-empty string")
    if service_type not in SERVICE_RATES:
        raise ValueError(f"Unknown service type: {service_type}")

    if history is None:
        history = []

    entry = {
        "type": service_type,
        "cost": SERVICE_RATES[service_type],
        "date": date.today().isoformat(),
    }
    service_records.setdefault(vehicle_no, []).append(entry)
    history.append(vehicle_no)
    return history


def cancel_service(vehicle_no, service_type):
    """Cancel matching jobs; return True only if a job was removed."""
    jobs = service_records.get(vehicle_no)
    if jobs is None:
        LOGGER.warning("No service records found for vehicle %s", vehicle_no)
        return False

    remaining = [job for job in jobs if job["type"] != service_type]
    service_records[vehicle_no] = remaining
    return len(remaining) < len(jobs)


def get_total_cost(vehicle_no):
    """Return the total cost of services for a vehicle."""
    return sum(job["cost"] for job in service_records.get(vehicle_no, []))


def job_card_id(vehicle_no):
    """Generate a stable, non-security identifier for a vehicle job card."""
    if not isinstance(vehicle_no, str) or not vehicle_no.strip():
        raise ValueError("vehicle_no must be a non-empty string")
    digest = hashlib.sha256(vehicle_no.encode("utf-8")).hexdigest()
    return digest[:8]


def busiest_vehicle():
    """Return the vehicle with most jobs, or None if there are no records."""
    if not service_records:
        return None
    return max(
        service_records,
        key=lambda vehicle: len(service_records[vehicle]),
    )


def save_records(file_name="services.json"):
    """Persist service records as JSON."""
    path = Path(file_name)
    with path.open("w", encoding="utf-8") as file_handle:
        json.dump(service_records, file_handle, indent=2)


def load_records(file_name="services.json"):
    """Load service records from JSON and check the top-level type."""
    path = Path(file_name)
    with path.open(encoding="utf-8") as file_handle:
        records = json.load(file_handle)
    if not isinstance(records, dict):
        raise ValueError("The records file must contain a JSON object")
    return records


def backup_records(folder):
    """Copy the records file to an existing destination directory."""
    source = Path("services.json")
    destination_dir = Path(folder)
    if not source.is_file():
        raise FileNotFoundError(
            "services.json does not exist; save records first"
        )
    if not destination_dir.is_dir():
        raise NotADirectoryError(
            f"Backup destination is not a directory: {folder}"
        )
    destination = destination_dir / source.name
    shutil.copy2(source, destination)
    LOGGER.info("Records backed up to %s", destination)
    return destination


def main():
    """Run the service-management demonstration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    add_service("KA01AB1234", "Oil Change")
    add_service("KA01AB1234", "Wheel Alignment")
    add_service("KA05XY9876")
    add_service("KA03MN4455", "Brake Check")
    cancel_service("KA05XY9876", "Brake Check")
    cancel_service("KA09ZZ0001", "General")
    cancel_service("KA03MN4455", "Brake Check")
    print(f"Total for KA01AB1234: {get_total_cost('KA01AB1234')}")
    print(f"Total for KA05XY9876: {get_total_cost('KA05XY9876')}")
    print(f"Job card for KA01AB1234: {job_card_id('KA01AB1234')}")
    save_records()
    loaded = load_records()
    print(
        f"Vehicles on file: {len(loaded)} | "
        f"busiest vehicle: {busiest_vehicle()}"
    )


if __name__ == "__main__":
    main()
