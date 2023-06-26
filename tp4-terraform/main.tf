provider "azurerm" {
  features {}
}

resource "azurerm_public_ip" "public_ip" {
  name                = "mypublicip"
  location            = "francecentral"
  resource_group_name = "ADDA84-CTP"
  allocation_method   = "Static"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "network-tp4"
  address_space       = ["10.3.0.0/16"]
  location            = "francecentral"
  resource_group_name = "ADDA84-CTP"
}

data "azurerm_subnet" "subnet" {
  name                 = "internal"
  resource_group_name  = "ADDA84-CTP"
  virtual_network_name = azurerm_virtual_network.vnet.name
  //address_prefixes     = ["10.3.0.0/16"]
}

resource "azurerm_network_interface" "nic" {
  name                      = "myinterface-20211331"
  location                  = "francecentral"
  resource_group_name       = "ADDA84-CTP"

  ip_configuration {
    name                          = "myconfig"
    subnet_id                     = data.azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public_ip.id
  }
}

resource "azurerm_network_security_group" "nsg" {
  name                = "mynsg"
  location            = "francecentral"
  resource_group_name = "ADDA84-CTP"
}

resource "azurerm_linux_virtual_machine" "vm" {
  name                = "devops-20211331"
  location            = "francecentral"
  resource_group_name = "ADDA84-CTP"
  network_interface_ids = [
    azurerm_network_interface.nic.id,
  ]
  size                = "Standard_D2s_v3"
  admin_username      = "devops"
  disable_password_authentication = true

  os_disk {
    name              = "osdisk-20211331"
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "16.04-LTS"
    version   = "latest"
  }


  admin_ssh_key {
    username = "devops"
    public_key =  file( "/Users/maisie/.ssh/id_rsa.pub")
  }
}

