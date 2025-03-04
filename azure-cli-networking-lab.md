# Chapter3 Lab 01 - Implement Virtual Networking (Using Azure CLI)

## Lab Introduction
This lab focuses on the basics of virtual networking and subnetting in Azure using the Azure CLI. You'll create virtual networks, subnets, network security groups (NSGs), application security groups (ASGs), and configure DNS zones. Estimated time: 50 minutes.

### Prerequisites
- Azure CLI installed (`az --version` to verify).
- An active Azure subscription.
- Region: East US (adjustable, but steps use `eastus`).

### Lab Scenario
Your organization is implementing virtual networks to support existing resources and future growth. You'll create:
- **CoreServicesVnet**: For core services with a large address space (10.20.0.0/16).
- **ManufacturingVnet**: For manufacturing systems with anticipated device growth (10.30.0.0/16).

## Task 1: Create a Virtual Network with Subnets
The organization anticipates significant growth in core services. You'll create the `CoreServicesVnet` with subnets using Azure CLI.

1. **Create the Resource Group**
   ```bash
   az group create --name az104-rg4 --location eastus
   ```

2. **Create the CoreServicesVnet**
   ```bash
   az network vnet create --resource-group az104-rg4 --name CoreServicesVnet --address-prefix 10.20.0.0/16 --location eastus
   ```

3. **Add Subnets**
   - SharedServicesSubnet (10.20.10.0/24):
     ```bash
     az network vnet subnet create --resource-group az104-rg4 --vnet-name CoreServicesVnet --name SharedServicesSubnet --address-prefix 10.20.10.0/24
     ```
   - DatabaseSubnet (10.20.20.0/24):
     ```bash
     az network vnet subnet create --resource-group az104-rg4 --vnet-name CoreServicesVnet --name DatabaseSubnet --address-prefix 10.20.20.0/24
     ```

4. **Verify the Virtual Network**
   ```bash
   az network vnet show --resource-group az104-rg4 --name CoreServicesVnet --query "{AddressSpace:addressSpace.addressPrefixes, Subnets:subnets[*].name}" --output table
   ```

5. **Export the Template (Optional)**
   - Export the configuration as an ARM template for Task 2:
     ```bash
     az group export --resource-group az104-rg4 --include-parameter-default-value > template.json
     ```
   - Manually download `template.json` from your terminal working directory for the next task.

## Task 2: Create a Virtual Network and Subnets Using a Template
You'll create `ManufacturingVnet` using an ARM template modified from Task 1.

1. **Edit the Exported Template**
   - Open `template.json` (from Task 1) in a text editor.
   - Replace all occurrences:
     - `CoreServicesVnet` → `ManufacturingVnet`
     - `10.20.0.0` → `10.30.0.0`
     - `SharedServicesSubnet` → `SensorSubnet1`
     - `10.20.10.0/24` → `10.30.20.0/24`
     - `DatabaseSubnet` → `SensorSubnet2`
     - `10.20.20.0/24` → `10.30.21.0/24`
   - Save the file as `manufacturing-template.json`.

2. **Deploy the Template**
   ```bash
   az deployment group create --resource-group az104-rg4 --template-file manufacturing-template.json
   ```

3. **Verify the Deployment**
   ```bash
   az network vnet show --resource-group az104-rg4 --name ManufacturingVnet --query "{AddressSpace:addressSpace.addressPrefixes, Subnets:subnets[*].name}" --output table
   ```

## Task 3: Create and Configure Communication Between an Application Security Group and a Network Security Group
You'll create an ASG and NSG, configure rules, and associate them with `CoreServicesVnet`.

1. **Create the Application Security Group (ASG)**
   ```bash
   az network asg create --resource-group az104-rg4 --name asg-web --location eastus
   ```

2. **Create the Network Security Group (NSG)**
   ```bash
   az network nsg create --resource-group az104-rg4 --name myNSGSecure --location eastus
   ```

3. **Associate NSG with SharedServicesSubnet**
   ```bash
   az network vnet subnet update --resource-group az104-rg4 --vnet-name CoreServicesVnet --name SharedServicesSubnet --network-security-group myNSGSecure
   ```

4. **Add Inbound Rule to Allow ASG Traffic (HTTP/HTTPS)**
   ```bash
   az network nsg rule create --resource-group az104-rg4 --nsg-name myNSGSecure --name AllowASG --priority 100 --source-asgs asg-web --destination-address-prefix "*" --destination-port-ranges 80 443 --access Allow --protocol Tcp --direction Inbound
   ```

5. **Add Outbound Rule to Deny Internet Access (Port 8080)**
   ```bash
   az network nsg rule create --resource-group az104-rg4 --nsg-name myNSGSecure --name DenyAnyCustom8080Outbound --priority 4096 --source-address-prefix "*" --destination-address-prefix "Internet" --destination-port-range 8080 --access Deny --protocol Any --direction Outbound
   ```

6. **Verify Rules**
   ```bash
   az network nsg rule list --resource-group az104-rg4 --nsg-name myNSGSecure --output table
   ```


## Cleanup Your Resources
To avoid unnecessary costs, delete the resource group:
```bash
az group delete --name az104-rg4 --yes --no-wait
```

## Key Takeaways
- Virtual networks in Azure support cloud-based networking with subnets for organization and security.
- Avoid overlapping IP ranges to simplify troubleshooting.
- NSGs control traffic with customizable rules; ASGs group servers by function.
- Azure DNS supports public and private name resolution.
