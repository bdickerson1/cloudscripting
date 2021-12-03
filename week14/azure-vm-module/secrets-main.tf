resource "azure_key_vault_secret" "example" {
    name = "NAME-of-KEY"
    value = "topsecretkey"
    key_vault_id = azurerm_key_vault.example.id
}