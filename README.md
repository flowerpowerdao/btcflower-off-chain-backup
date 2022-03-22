# usage
- run `poetry install` from the current directory
- run `poetry run backup <canister_id>` to execute the backup functionality
- this will execute a scheduler that updates the `registry.json` and `tokens.json` files every 60 minutes with live data from the canister