# Athena Health MCP Server

A Model Context Protocol (MCP) server for integrating with Athena Health's API to manage appointments, providers, departments, and patient data.

## Overview

This MCP server provides tools for:
- Appointment management (create, update, cancel, view)
- Provider and department information
- Patient search functionality
- Available appointment slot discovery

## Setup

### Prerequisites

1. Python 3.8+
2. Required environment variables:
   - `ATHENA_CLIENT_ID`: Your Athena Health API client ID
   - `ATHENA_CLIENT_SECRET`: Your Athena Health API client secret
   - `ATHENA_PRACTICE_ID`: Your practice ID
   - `ATHENA_BASE_URL`: (Optional) API base URL (defaults to production)

### Installation

1. Install dependencies:
```bash
pip install aiohttp python-dotenv mcp
```

2. Set environment variables:
```bash
export ATHENA_CLIENT_ID='your_client_id'
export ATHENA_CLIENT_SECRET='your_client_secret'
export ATHENA_PRACTICE_ID='your_practice_id'
export ATHENA_BASE_URL='https://api.athenahealth.com'  # Optional
```

3. Run the server:
```bash
python main.py
```

## Available Tools

### 1. get_appointments

Retrieve appointments for a specific date range with optional filtering.

**Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format
- `provider_id` (optional): Provider ID to filter appointments
- `department_id` (optional): Department ID to filter appointments

**Example:**
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "provider_id": "12345"
}
```

### 2. get_available_slots

Get available appointment slots for scheduling.

**Parameters:**
- `provider_id` (required): Provider ID
- `department_id` (required): Department ID
- `appointment_type_id` (required): Appointment type ID
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format

**Example:**
```json
{
  "provider_id": "12345",
  "department_id": "67890",
  "appointment_type_id": "11111",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

### 3. create_appointment

Create a new appointment.

**Parameters:**
- `patient_id` (required): Patient ID
- `provider_id` (required): Provider ID
- `department_id` (required): Department ID
- `appointment_type_id` (required): Appointment type ID
- `appointment_date` (required): Appointment date in YYYY-MM-DD format
- `appointment_time` (required): Appointment time in HH:MM format
- `reason_for_visit` (optional): Reason for the visit

**Example:**
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

### 4. update_appointment

Update an existing appointment.

**Parameters:**
- `appointment_id` (required): Appointment ID to update
- `appointment_date` (optional): New appointment date in YYYY-MM-DD format
- `appointment_time` (optional): New appointment time in HH:MM format
- `reason_for_visit` (optional): Updated reason for the visit
- `notes` (optional): Additional notes

**Example:**
```json
{
  "appointment_id": "55555",
  "appointment_date": "2024-01-16",
  "appointment_time": "15:00",
  "reason_for_visit": "Follow-up appointment",
  "notes": "Patient requested time change"
}
```

### 5. cancel_appointment

Cancel an appointment.

**Parameters:**
- `appointment_id` (required): Appointment ID to cancel
- `cancellation_reason` (optional): Reason for cancellation

**Example:**
```json
{
  "appointment_id": "55555",
  "cancellation_reason": "Patient requested cancellation"
}
```

### 6. get_providers

Get list of providers with optional filtering.

**Parameters:**
- `department_id` (optional): Department ID to filter providers
- `specialty` (optional): Specialty to filter providers

**Example:**
```json
{
  "department_id": "67890",
  "specialty": "Cardiology"
}
```

### 7. get_departments

Get list of all departments.

**Parameters:**
None

**Example:**
```json
{}
```

### 8. get_appointment_types

Get available appointment types with optional filtering.

**Parameters:**
- `department_id` (optional): Department ID to filter appointment types
- `provider_id` (optional): Provider ID to filter appointment types

**Example:**
```json
{
  "department_id": "67890",
  "provider_id": "12345"
}
```

### 9. search_patients

Search for patients by various criteria.

**Parameters:**
- `first_name` (optional): Patient first name
- `last_name` (optional): Patient last name
- `date_of_birth` (optional): Date of birth in YYYY-MM-DD format
- `phone` (optional): Phone number
- `email` (optional): Email address

**Example:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-01"
}
```

## API Endpoints

The server interacts with the following Athena Health API endpoints:

- `POST /oauth2/v1/token` - Authentication
- `GET /v1/{practice_id}/appointments` - Get appointments
- `GET /v1/{practice_id}/appointments/open` - Get available slots
- `POST /v1/{practice_id}/appointments` - Create appointment
- `PUT /v1/{practice_id}/appointments/{id}` - Update appointment
- `GET /v1/{practice_id}/providers` - Get providers
- `GET /v1/{practice_id}/departments` - Get departments
- `GET /v1/{practice_id}/appointmenttypes` - Get appointment types
- `GET /v1/{practice_id}/patients` - Search patients

## Authentication

The server automatically handles OAuth2 authentication using client credentials flow. Tokens are cached and refreshed as needed.

## Error Handling

The server includes comprehensive error handling for:
- Authentication failures
- API request failures
- Invalid parameters
- Network errors

All errors are logged and returned as part of the tool response.

## Usage Examples

### Complete Workflow Example

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

5. **Search for a patient:**
```json
{
  "tool": "search_patients",
  "arguments": {
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

6. **Create an appointment:**
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

## Response Format

All tool responses are returned as JSON strings containing the API response data. For example:

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
      "status": "scheduled"
    }
  ]
}
```

## Troubleshooting

### Common Issues

1. **Authentication Errors:**
   - Verify your `ATHENA_CLIENT_ID` and `ATHENA_CLIENT_SECRET` are correct
   - Ensure your API credentials have the necessary permissions

2. **Missing Environment Variables:**
   - The server will exit with an error message listing missing variables
   - Set all required environment variables before running

3. **API Request Failures:**
   - Check that your `ATHENA_PRACTICE_ID` is correct
   - Verify the API endpoints are accessible from your network
   - Review the error response for specific API error messages

### Logging

The server logs all operations at INFO level. Check the console output for detailed information about:
- Authentication attempts
- API requests and responses
- Error details

## Security Considerations

- Never commit API credentials to version control
- Use environment variables for all sensitive configuration
- The server automatically handles token refresh and secure storage
- All API communication uses HTTPS

## Support

For issues with the MCP server implementation, check the logs for detailed error messages. For Athena Health API-specific issues, refer to the official Athena Health API documentation. # athenahealth-mcp
