# ER Diagram for ProofLog

## Entities

### 1. User
| Attribute | Type | Constraints |
|-----------|------|-------------|
| id | Integer | PK, Auto Increment |
| email | String | Unique, Not Null |
| password | String | Not Null (Hashed) |
| role | String | default='intern' |

### 2. Project
| Attribute | Type | Constraints |
|-----------|------|-------------|
| id | Integer | PK, Auto Increment |
| user_id | Integer | FK -> User.id |
| name | String | Not Null |
| description | Text | Optional |
| created_at | DateTime | Auto Now Add |

### 3. Log
| Attribute | Type | Constraints |
|-----------|------|-------------|
| id | Integer | PK, Auto Increment |
| project_id | Integer | FK -> Project.id |
| date | Date | Not Null |
| hours | Float | Positive |
| description | Text | Not Null |
| is_approved | Boolean | Default False |

### 4. Proof
| Attribute | Type | Constraints |
|-----------|------|-------------|
| id | Integer | PK, Auto Increment |
| log_id | Integer | FK -> Log.id |
| file_path | String(500) | Local Storage Path |
| uploaded_at | DateTime | Auto Now Add |

## Relationships

- **User** (1) ----< (N) **Project**
  - One User creates many Projects.
  - A Project belongs to exactly one User.

- **Project** (1) ----< (N) **Log**
  - One Project contains many Logs.
  - A Log belongs to exactly one Project.

- **Log** (1) ----< (0..1) **Proof**
  - One Log can have 0 or 1 Proof (Optional upload).
  - A Proof belongs to exactly one Log.

## Textual Diagram

```mermaid
erDiagram
    User ||--o{ Project : owns
    Project ||--o{ Log : contains
    Log ||--o| Proof : has_evidence

    User {
        int id PK
        string email
        string password
        string role
    }

    Project {
        int id PK
        int user_id FK
        string name
        text description
        datetime created_at
    }

    Log {
        int id PK
        int project_id FK
        date date
        float hours
        text description
        boolean is_approved
    }

    Proof {
        int id PK
        int log_id FK
        string file_path
        datetime uploaded_at
    }
```
