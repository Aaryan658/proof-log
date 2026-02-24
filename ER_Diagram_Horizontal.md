# Horizontal ER Diagram for ProofLog

This is a representation of the ProofLog Entity-Relationship (ER) diagram using standard ER notation: Rectangles for Entities (Tables), Diamonds for Relationships, and Ovals for Attributes (underlined for Primary Keys).

```mermaid
flowchart LR
    %% Entities (Rectangles)
    E_User[User]
    E_Project[Project]
    E_Log[Log]
    E_Proof[Proof]

    %% Relationships (Diamonds)
    R_owns{Owns}
    R_contains{Contains}
    R_has{Has}

    %% User Attributes (Ovals)
    A_U_id([id])
    A_U_email([email])
    A_U_pass([password])
    A_U_role([role])

    %% Project Attributes (Ovals)
    A_P_id([id])
    A_P_uid([user_id])
    A_P_name([name])
    A_P_desc([description])
    A_P_created([created_at])

    %% Log Attributes (Ovals)
    A_L_id([id])
    A_L_pid([project_id])
    A_L_date([date])
    A_L_hours([hours])
    A_L_desc([description])
    A_L_approv([is_approved])

    %% Proof Attributes (Ovals)
    A_Pr_id([id])
    A_Pr_lid([log_id])
    A_Pr_path([file_path])
    A_Pr_up([uploaded_at])

    %% Apply Underline Styling for Primary Keys
    style A_U_id text-decoration:underline;
    style A_P_id text-decoration:underline;
    style A_L_id text-decoration:underline;
    style A_Pr_id text-decoration:underline;

    %% Connect Attributes to Entities
    A_U_id --- E_User
    E_User --- A_U_email
    E_User --- A_U_pass
    E_User --- A_U_role

    A_P_id --- E_Project
    E_Project --- A_P_uid
    E_Project --- A_P_name
    E_Project --- A_P_desc
    E_Project --- A_P_created

    A_L_id --- E_Log
    E_Log --- A_L_pid
    E_Log --- A_L_date
    E_Log --- A_L_hours
    E_Log --- A_L_desc
    E_Log --- A_L_approv

    A_Pr_id --- E_Proof
    E_Proof --- A_Pr_lid
    E_Proof --- A_Pr_path
    E_Proof --- A_Pr_up

    %% Connect Entities through Relationships
    E_User ---|1| R_owns
    R_owns ---|N| E_Project

    E_Project ---|1| R_contains
    R_contains ---|N| E_Log

    E_Log ---|1| R_has
    R_has ---|0..1| E_Proof
```

