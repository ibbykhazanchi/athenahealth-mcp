# Athena Health MCP API Documentation

This document provides detailed information about each tool available in the Athena Health MCP server, including parameters, response formats, and usage examples.

## Table of Contents

1. [Appointment Management](#appointment-management)
2. [Provider & Department Management](#provider--department-management)
3. [Patient Management](#patient-management)
4. [Error Handling](#error-handling)
5. [Response Formats](#response-formats)

## Appointment Management

### 1. get_appointments

Retrieves appointments for a specified date range with optional filtering by provider or department.

**Tool Name:** `get_appointments`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start_date` | string | Yes | Start date in YYYY-MM-DD format |
| `end_date` | string | Yes | End date in YYYY-MM-DD format |
| `provider_id` | string | No | Provider ID to filter appointments |
| `department_id` | string | No | Department ID to filter appointments |

**Example Request:**
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "provider_id": "12345",
  "department_id": "67890"
}
```

**Example Response:**
```json
{
  "appointments": [
    {
      "appointmentid": "55555",
      "patientid": "99999",
      "providerid": "12345",
      "departmentid": "67890",
      "appointmentdate": "2024-01-15",
      "appointmenttime": "14:30",
      "appointmenttype": "Annual Checkup",
      "status": "scheduled",
      "patientname": "John Doe",
      "providername": "Dr. Smith"
    }
  ],
  "totalcount": 1
}
```

### 2. get_available_slots

Retrieves available appointment slots for scheduling based on provider, department, and appointment type.

**Tool Name:** `get_available_slots`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `provider_id` | string | Yes | Provider ID |
| `department_id` | string | Yes | Department ID |
| `appointment_type_id` | string | Yes | Appointment type ID |
| `start_date` | string | Yes | Start date in YYYY-MM-DD format |
| `end_date` | string | Yes | End date in YYYY-MM-DD format |

**Example Request:**
```json
{
  "provider_id": "12345",
  "department_id": "67890",
  "appointment_type_id": "11111",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

**Example Response:**
```json
{
  "slots": [
    {
      "date": "2024-01-15",
      "time": "09:00",
      "duration": 30,
      "available": true
    },
    {
      "date": "2024-01-15",
      "time": "14:30",
      "duration": 30,
      "available": true
    }
  ]
}
```

### 3. create_appointment

Creates a new appointment with the specified parameters.

**Tool Name:** `create_appointment`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `patient_id` | string | Yes | Patient ID |
| `provider_id` | string | Yes | Provider ID |
| `department_id` | string | Yes | Department ID |
| `appointment_type_id` | string | Yes | Appointment type ID |
| `appointment_date` | string | Yes | Appointment date in YYYY-MM-DD format |
| `appointment_time` | string | Yes | Appointment time in HH:MM format |
| `reason_for_visit` | string | No | Reason for the visit |

**Example Request:**
```json
{
  "patient_id": "99999",
  "provider_id": "12345",
  "department_id": "67890",
  "appointment_type_id": "11111",
  "appointment_date": "2024-01-15",
  "appointment_time": "14:30",
  "reason_for_visit": "Annual checkup"
}
```

**Example Response:**
```json
{
  "appointmentid": "66666",
  "status": "scheduled",
  "message": "Appointment created successfully"
}
```

### 4. update_appointment

Updates an existing appointment with new information.

**Tool Name:** `update_appointment`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `appointment_id` | string | Yes | Appointment ID to update |
| `appointment_date` | string | No | New appointment date in YYYY-MM-DD format |
| `appointment_time` | string | No | New appointment time in HH:MM format |
| `reason_for_visit` | string | No | Updated reason for the visit |
| `notes` | string | No | Additional notes |

**Example Request:**
```json
{
  "appointment_id": "55555",
  "appointment_date": "2024-01-16",
  "appointment_time": "15:00",
  "reason_for_visit": "Follow-up appointment",
  "notes": "Patient requested time change"
}
```

**Example Response:**
```json
{
  "appointmentid": "55555",
  "status": "updated",
  "message": "Appointment updated successfully"
}
```

### 5. cancel_appointment

Cancels an existing appointment.

**Tool Name:** `cancel_appointment`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `appointment_id` | string | Yes | Appointment ID to cancel |
| `cancellation_reason` | string | No | Reason for cancellation |

**Example Request:**
```json
{
  "appointment_id": "55555",
  "cancellation_reason": "Patient requested cancellation"
}
```

**Example Response:**
```json
{
  "appointmentid": "55555",
  "status": "cancelled",
  "message": "Appointment cancelled successfully"
}
```

## Provider & Department Management

### 6. get_providers

Retrieves a list of providers with optional filtering by department or specialty.

**Tool Name:** `get_providers`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `department_id` | string | No | Department ID to filter providers |
| `specialty` | string | No | Specialty to filter providers |

**Example Request:**
```json
{
  "department_id": "67890",
  "specialty": "Cardiology"
}
```

**Example Response:**
```json
{
  "providers": [
    {
      "providerid": "12345",
      "firstname": "John",
      "lastname": "Smith",
      "specialty": "Cardiology",
      "departmentid": "67890",
      "active": true
    },
    {
      "providerid": "12346",
      "firstname": "Jane",
      "lastname": "Doe",
      "specialty": "Cardiology",
      "departmentid": "67890",
      "active": true
    }
  ],
  "totalcount": 2
}
```

### 7. get_departments

Retrieves a list of all departments.

**Tool Name:** `get_departments`

**Parameters:** None

**Example Request:**
```json
{}
```

**Example Response:**
```json
{
  "departments": [
    {
      "departmentid": "67890",
      "name": "Cardiology",
      "active": true
    },
    {
      "departmentid": "67891",
      "name": "Primary Care",
      "active": true
    }
  ],
  "totalcount": 2
}
```

### 8. get_appointment_types

Retrieves available appointment types with optional filtering by department or provider.

**Tool Name:** `get_appointment_types`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `department_id` | string | No | Department ID to filter appointment types |
| `provider_id` | string | No | Provider ID to filter appointment types |

**Example Request:**
```json
{
  "department_id": "67890",
  "provider_id": "12345"
}
```

**Example Response:**
```json
{
  "appointmenttypes": [
    {
      "appointmenttypeid": "11111",
      "name": "Annual Checkup",
      "duration": 30,
      "departmentid": "67890",
      "active": true
    },
    {
      "appointmenttypeid": "11112",
      "name": "Follow-up Visit",
      "duration": 15,
      "departmentid": "67890",
      "active": true
    }
  ],
  "totalcount": 2
}
```

## Patient Management

### 9. search_patients

Searches for patients using various criteria.

**Tool Name:** `search_patients`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `first_name` | string | No | Patient first name |
| `last_name` | string | No | Patient last name |
| `date_of_birth` | string | No | Date of birth in YYYY-MM-DD format |
| `phone` | string | No | Phone number |
| `email` | string | No | Email address |

**Example Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-01"
}
```

**Example Response:**
```json
{
  "patients": [
    {
      "patientid": "99999",
      "firstname": "John",
      "lastname": "Doe",
      "dob": "1990-01-01",
      "homephone": "555-123-4567",
      "email": "john.doe@email.com",
      "active": true
    }
  ],
  "totalcount": 1
}
```

## Error Handling

The MCP server includes comprehensive error handling for various scenarios:

### Authentication Errors
```json
{
  "error": "Authentication failed: 401 - Invalid credentials"
}
```

### API Request Errors
```json
{
  "error": "API request failed: 400 - Invalid parameters"
}
```

### Missing Parameters
```json
{
  "error": "Missing required parameter: start_date"
}
```

### Network Errors
```json
{
  "error": "Network error: Connection timeout"
}
```

## Response Formats

All successful responses follow a consistent JSON format:

### List Responses
```json
{
  "items": [...],
  "totalcount": 1,
  "next": "token_for_pagination"
}
```

### Single Item Responses
```json
{
  "item": {...},
  "status": "success"
}
```

### Action Responses
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "id": "generated_id"
}
```

## Common Workflows

### Complete Appointment Scheduling Workflow

1. **Get departments:**
```json
{"tool": "get_departments", "arguments": {}}
```

2. **Get providers in a department:**
```json
{"tool": "get_providers", "arguments": {"department_id": "67890"}}
```

3. **Get appointment types:**
```json
{"tool": "get_appointment_types", "arguments": {"department_id": "67890"}}
```

4. **Search for available slots:**
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

5. **Search for patient:**
```json
{
  "tool": "search_patients",
  "arguments": {
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

6. **Create appointment:**
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

### Appointment Management Workflow

1. **Get existing appointments:**
```json
{
  "tool": "get_appointments",
  "arguments": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  }
}
```

2. **Update appointment:**
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

3. **Cancel appointment (if needed):**
```json
{
  "tool": "cancel_appointment",
  "arguments": {
    "appointment_id": "55555",
    "cancellation_reason": "Patient requested cancellation"
  }
}
```

## Best Practices

1. **Error Handling:** Always check for error responses and handle them appropriately
2. **Parameter Validation:** Ensure all required parameters are provided
3. **Date Formats:** Use YYYY-MM-DD format for dates and HH:MM format for times
4. **Authentication:** The server handles authentication automatically, but ensure credentials are valid
5. **Rate Limiting:** Be mindful of API rate limits when making multiple requests
6. **Data Privacy:** Handle patient data according to HIPAA guidelines

## Troubleshooting

### Common Issues and Solutions

1. **Authentication Failures:**
   - Verify API credentials are correct
   - Check that credentials have necessary permissions
   - Ensure practice ID is valid

2. **Invalid Parameters:**
   - Verify date formats (YYYY-MM-DD)
   - Check that IDs exist in the system
   - Ensure required parameters are provided

3. **No Results:**
   - Check date ranges are valid
   - Verify provider/department IDs exist
   - Ensure search criteria are specific enough

4. **Network Issues:**
   - Check internet connectivity
   - Verify API endpoints are accessible
   - Check firewall settings 