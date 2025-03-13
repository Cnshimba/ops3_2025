# Homework: Implementing a Three-Tier Architecture in Azure

## Overview

In this homework, you will design and implement a secure three-tier architecture in Azure using Infrastructure as Code (ARM templates). Starting from scratch, you will create a complete network infrastructure with proper security controls and load balancing for a web application. The architecture must include web servers, application servers, and database servers, each in their own network tier with appropriate security boundaries.

## Learning Objectives

By completing this assignment, you will:
- Design and implement a multi-tier application architecture in Azure
- Create and configure Application Security Groups (ASGs) for fine-grained network security
- Develop Network Security Groups (NSGs) with proper rules based on the principle of least privilege
- Configure Azure Load Balancer to distribute traffic to web servers
- Gain practical experience writing Azure ARM templates from scratch

## Requirements

Create an ARM template that implements the following architecture:

### 1. Network Infrastructure
- Create a Virtual Network with address space 10.0.0.0/16
- Create three subnets:
  - Web tier subnet (10.0.1.0/24)
  - Application tier subnet (10.0.2.0/24)
  - Database tier subnet (10.0.3.0/24)
- Apply a single Network Security Group to all subnets

### 2. Security Groups
- Create three Application Security Groups (ASGs), one for each tier:
  - Web servers ASG
  - Application servers ASG
  - Database servers ASG
- Configure a Network Security Group with rules that:
  - Allow HTTP (80) and HTTPS (443) traffic from the internet to the web tier ASG
  - Allow HTTPS (443) traffic from the web tier ASG to the application tier ASG
  - Allow SQL Server (1433) traffic from the application tier ASG to the database tier ASG
  - Deny all other inbound traffic

### 3. Load Balancer
- Create a public-facing Azure Load Balancer for the web tier
- Configure the load balancer with:
  - A public IP address
  - A backend pool for web servers
  - Health probes for HTTP and HTTPS
  - Load balancing rules for ports 80 and 443

### 4. Virtual Machine Planning
- DO NOT implement the actual VMs, but your ARM template should be designed to accommodate:
  - 3 VMs for each tier (web, application, database)
  - Each VM should be assigned to its appropriate ASG
  - Web tier VMs should be configured to join the load balancer's backend pool

## Deliverables

1. A complete ARM template (JSON file) that implements all requirements from scratch
2. A brief document (2-3 pages) explaining:
   - Your approach to designing the architecture
   - Key design decisions you made and why
   - How the security rules enforce the principle of least privilege
   - How you would implement the VMs if that were part of the assignment
   - How you would improve the architecture for a production environment

## Submission Guidelines

- Submit all files through the course management system
- Ensure your ARM template validates successfully before submission
- Make sure your document is in PDF format

## Due Date

The assignment is due on [21/3/2025].

## Additional Resources

- [Azure Virtual Network documentation](https://docs.microsoft.com/en-us/azure/virtual-network/)
- [Application Security Groups overview](https://docs.microsoft.com/en-us/azure/virtual-network/application-security-groups)
- [Azure Load Balancer documentation](https://docs.microsoft.com/en-us/azure/load-balancer/)
- [ARM template reference](https://docs.microsoft.com/en-us/azure/templates/)

# Homework Grading Rubric

## ARM Template Design and Implementation (70 points)

### Network Infrastructure (20 points)
| Criteria | Points | Description |
|----------|--------|-------------|
| Virtual Network Design | 5 | Virtual network correctly configured with appropriate address space |
| Subnet Configuration | 5 | Three subnets created with appropriate address ranges and naming |
| NSG Design | 5 | NSG structure correctly designed and applied to subnets |
| Resource Parameterization | 5 | Effective parameterization of network resources for flexibility |

### Security Implementation (25 points)
| Criteria | Points | Description |
|----------|--------|-------------|
| ASG Creation | 8 | Three ASGs correctly created for each tier with appropriate names |
| Internet to Web Tier Rules | 5 | Correct implementation of rules allowing HTTP/HTTPS from internet to web tier ASG |
| Web to App Tier Rules | 5 | Correct implementation of rules allowing HTTPS from web tier ASG to app tier ASG |
| App to DB Tier Rules | 5 | Correct implementation of rules allowing SQL traffic from app tier ASG to database tier ASG |
| Deny All Rule | 2 | Correctly implemented default deny rule for all other traffic |

### Load Balancer Configuration (15 points)
| Criteria | Points | Description |
|----------|--------|-------------|
| Public IP Configuration | 3 | Correctly configured public IP for the load balancer |
| Frontend Configuration | 3 | Properly configured frontend IP configuration |
| Backend Pool Setup | 3 | Backend pool correctly defined for web tier VMs |
| Health Probes | 3 | HTTP and HTTPS health probes properly configured |
| Load Balancing Rules | 3 | Rules correctly implemented for HTTP and HTTPS traffic |

### Template Quality and Best Practices (10 points)
| Criteria | Points | Description |
|----------|--------|-------------|
| Template Structure | 3 | Well-organized, logical template structure |
| Parameter Design | 3 | Appropriate use of parameters with defaults and constraints |
| Output Design | 2 | Useful outputs for resource references |
| Resource Dependencies | 2 | Correct implementation of resource dependencies |

## Documentation (30 points)

### Architecture Design (15 points)
| Criteria | Points | Description |
|----------|--------|-------------|
| Design Approach | 5 | Clear explanation of architectural design approach |
| Security Design Rationale | 5 | Well-justified security design decisions |
| Technical Accuracy | 5 | Technically accurate explanations of Azure concepts |

### VM Implementation Plan (10 points)
| Criteria | Points | Description |
|----------|--------|-------------|
| VM Configuration Planning | 5 | Detailed explanation of how VMs would be implemented |
| ASG and LB Integration | 5 | Clear explanation of how VMs would be integrated with ASGs and load balancer |

### Production Improvements (5 points)
| Criteria | Points | Description |
|----------|--------|-------------|
| Improvement Suggestions | 5 | Relevant, realistic, and detailed suggestions for production environment |

## Total: 100 points

### Grading Scale
| Grade | Points |
|-------|--------|
| A     | 90-100 |
| B     | 80-89  |
| C     | 70-79  |
| D     | 60-69  |
| F     | <60    |

### Additional Notes for Graders:
- Templates that fail to validate will receive a maximum of 50 points
- Security implementations that leave significant vulnerabilities will be capped at 60 points
- Exceptional work demonstrating advanced understanding or innovative solutions may receive up to 5 bonus points
