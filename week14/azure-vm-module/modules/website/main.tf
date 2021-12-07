#Create Storage account
resource "azurerm_storage_account" "storage_account" {
  name                = "staticwebsitebdickerson1"
  resource_group_name = var.resourceGroupName
 
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  allow_blob_public_access = true
 
  static_website {
    index_document = "index.html"
  }
}
resource "azurerm_storage_container" "container" {
  name                  = "web"
  storage_account_name  = azurerm_storage_account.storage_account.name
  container_access_type = "blob"
}
#Add index.html to blob storage
resource "azurerm_storage_blob" "example" {
  name                   = "index.html"
  storage_account_name   = azurerm_storage_account.storage_account.name
  storage_container_name = azurerm_storage_container.container.name
  type                   = "Block"
  content_type           = "text/html"
  source_content         = "<h1>This is static content for Ben Dickerson's website</h1>"
}