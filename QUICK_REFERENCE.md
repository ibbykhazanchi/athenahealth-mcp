# Athena Health MCP Quick Reference

## Quick Start

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ATHENA_CLIENT_ID='your_client_id'
export ATHENA_CLIENT_SECRET='your_client_secret'
export ATHENA_PRACTICE_ID='your_practice_id'

# Run server
python main.py
```

## Common Operations

### 1. Get Appointments
```json
{
  "tool": "get_appointments",
  "arguments": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  }
}
```

### 2. Create Appointment
```json
{
  "tool": "create_appointment",
  "arguments": {
    "patient_id": "99999",
    "provider_id": "12345",
    "department_id": "67890",
    "appointment_type_id": "11111",
    "appointment_date": "2024-01-15",
    "appointment_time": "14:30",
    "reason_for_visit": "Annual checkup"
  }
}
```

### 3. Search Patients
```json
{
  "tool": "search_patients",
  "arguments": {
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### 4. Get Available Slots
```json
{
  "tool": "get_available_slots",
  "arguments": {
    "provider_id": "12345",
    "department_id": "67890",
    "appointment_type_id": "11111",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  }
}
```

### 5. Update Appointment
```json
{
  "tool": "update_appointment",
  "arguments": {
    "appointment_id": "55555",
    "appointment_date": "2024-01-16",
    "appointment_time": "15:00"
  }
}
```

### 6. Cancel Appointment
```json
{
  "tool": "cancel_appointment",
  "arguments": {
    "appointment_id": "55555",
    "cancellation_reason": "Patient requested cancellation"
  }
}
```

## Reference Tables

### Required Parameters by Tool

| Tool | Required Parameters |
|------|-------------------|
| `get_appointments` | `start_date`, `end_date` |
| `get_available_slots` | `provider_id`, `department_id`, `appointment_type_id`, `start_date`, `end_date` |
| `create_appointment` | `patient_id`, `provider_id`, `department_id`, `appointment_type_id`, `appointment_date`, `appointment_time` |
| `update_appointment` | `appointment_id` |
| `cancel_appointment` | `appointment_id` |
| `get_providers` | None |
| `get_departments` | None |
| `get_appointment_types` | None |
| `search_patients` | None (but at least one search criteria recommended) |

### Date/Time Formats

| Field | Format | Example |
|-------|--------|---------|
| Date | YYYY-MM-DD | "2024-01-15" |
| Time | HH:MM | "14:30" |
| Date of Birth | YYYY-MM-DD | "1990-01-01" |

### Common Error Codes

| Error | Description | Solution |
|-------|-------------|----------|
| `Authentication failed` | Invalid credentials | Check ATHENA_CLIENT_ID and ATHENA_CLIENT_SECRET |
| `Missing required parameter` | Required field not provided | Add missing parameter |
| `API request failed: 400` | Invalid parameters | Check parameter values and formats |
| `API request failed: 404` | Resource not found | Verify IDs exist in system |

## Workflow Templates

### New Patient Appointment
1. Search for patient → `search_patients`
2. Get departments → `get_departments`
3. Get providers → `get_providers`
4. Get appointment types → `get_appointment_types`
5. Get available slots → `get_available_slots`
6. Create appointment → `create_appointment`

### Existing Patient Appointment
1. Search for patient → `search_patients`
2. Get available slots → `get_available_slots`
3. Create appointment → `create_appointment`

### Appointment Management
1. Get appointments → `get_appointments`
2. Update appointment → `update_appointment` (if needed)
3. Cancel appointment → `cancel_appointment` (if needed)

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ATHENA_CLIENT_ID` | Yes | Your Athena Health API client ID |
| `ATHENA_CLIENT_SECRET` | Yes | Your Athena Health API client secret |
| `ATHENA_PRACTICE_ID` | Yes | Your practice ID |
| `ATHENA_BASE_URL` | No | API base URL (defaults to production) |

## Response Examples

### Successful Response
```json
{
  "appointments": [
    {
      "appointmentid": "55555",
      "patientid": "99999",
      "providerid": "12345",
      "appointmentdate": "2024-01-15",
      "appointmenttime": "14:30",
      "status": "scheduled"
    }
  ],
  "totalcount": 1
}
```

### Error Response
```json
{
  "error": "Authentication failed: 401 - Invalid credentials"
}
``` 