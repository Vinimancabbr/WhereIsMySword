import json
import os

inventoryFile = "inventory.json"
keepRunning = True

#Load json inventory files in json format, 
def loadInventoryFile():
    if not os.path.exists(inventoryFile):
        return {}
    with open(inventoryFile, "r", encoding="utf-8") as f:
        return json.load(f)

def saveInventoryData(Data):
    with open(inventoryFile, "w", encoding="utf-8") as f:
        json.dump(Data, f, ensure_ascii=False, indent=4)
        
        
def generateId(data):
    maxId = 0
    for v in data.values():
        actualId = v.get("id")
        if actualId and actualId.isdigit():
            maxId = max(maxId, int(actualId))
    return f"{maxId + 1}"       

# ===========================
#  CHARACTER MANAGEMENT
# ===========================

def createCharacter(name):
    data = loadInventoryFile()
    if name in data:
        print(f"⚠️ The character 🧙 '{name}' already exists.")
        return
    newId = generateId(data)
    data[name] = {"id": newId, "inventory": {}}
    saveInventoryData(data)
    print(f"✅ 🧙 '{name}' joined the 🤝 party!")
    
def editCharacter():
    character = selectCharacter("Which 🧙 character do you want to edit?")
    if not character:
        return

    data = loadInventoryFile()
    new_name = input(f"Enter new name for 🧙 '{character}': ").strip()
    if not new_name:
        print("❌ Name cannot be empty.")
        return
    if new_name in data:
        print(f"⚠️ A character named 🧙 '{new_name}' already exists.")
        return

    # Rename character key in dictionary
    data[new_name] = data.pop(character)
    saveInventoryData(data)
    print(f"✅ Character 🧙 '{character}' is now 🧙 '{new_name}'.")

def deleteCharacter(name):
    data = loadInventoryFile()
    if name not in data:
        print(f"❌ The character 🧙 '{name}' doesn't exist.")
        return

    confirm = input(f"Are you sure you want to delete 🧙 '{name}'? (y/n): ").strip().lower()
    if confirm != "y":
        print(f"🧙'{name}' was spared.")
        return

    del data[name]
    saveInventoryData(data)
    print(f"💀 '{name}' has been removed from the party.")  
    

def selectCharacter(prompt="Select a 🧙 character: "):
    data = loadInventoryFile()
    if not data:
        print("❌ No characters available.")
        return None

    showParty()
    choice = input(f"{prompt} ").strip()

    # Try to find by ID
    for name, info in data.items():
        if choice == info["id"] or choice.lower() == name.lower():
            return name

    print("❌ Invalid 🧙 character selection.")
    return None

def showParty():
    data = loadInventoryFile()
    if not data:
        print("❌ The party is empty!")
        return

    print("\n=== 🧙🤝 Party Members 🤝🧙 ===")
    for name, info in data.items():
        print(f"{info['id']} - 🧙 {name}")
        
# ===========================
#  INVENTORY MANAGEMENT
# ===========================
def addItem(character, itemName, quantity, description=""):
    data = loadInventoryFile()
    if character not in data:
        print(f"❌ The character 🧙 '{character}' doesn't exist.")
        return

    inventory = data[character]["inventory"]

    if itemName in inventory:
        inventory[itemName]["quantity"] += quantity
    else:
        newId = generateId(inventory)
        inventory[itemName] = {
            "id": newId,
            "quantity": quantity,
            "description": description
        }

    saveInventoryData(data)
    print(f"✅ '{itemName}' was added to 🧙 '{character}'s 🎒 inventory.")

def editItem():
    character = selectCharacter("Select the 🧙 character whose item you want to edit:")
    if not character:
        return
    
    item = selectItem(character)
    if not item:
        return

    data = loadInventoryFile()
    inventory = data[character]["inventory"]
    current = inventory[item]

    print(f"\nEditing 📦 '{item}' (ID: {current['id']}) in 🧙 {character}'s 🎒 inventory:")
    new_name = input(f"New name (leave empty to keep '{item}'): ").strip()
    new_qty = input(f"New quantity (current {current['quantity']}): ").strip()
    new_desc = input(f"New description (leave empty to keep current): ").strip()

    # Update fields
    if new_name:
        # Rename the key in dictionary
        inventory[new_name] = inventory.pop(item)
        item = new_name  # update reference for saving
    if new_qty.isdigit():
        inventory[item]["quantity"] = int(new_qty)
    if new_desc:
        inventory[item]["description"] = new_desc

    saveInventoryData(data)
    print(f"✅ Item 📦 '{item}' updated successfully in 🧙 {character}'s 🎒  inventory.")

def removeItem(character, itemName):
    data = loadInventoryFile()
    if character not in data:
        print(f"❌ The character 🧙 '{character}' doesn't exist.")
        return

    inventory = data[character]["inventory"]

    if itemName in inventory:
        del inventory[itemName]
        saveInventoryData(data)
        print(f"🗑️ '{itemName}' was removed from 🧙 '{character}'s 🎒 inventory.")
    else:
        print(f"⚠️ '{character}' doesn't have the item 📦 '{itemName}'.")
        
def tradeItems(origin, destiny, itemName, quantity):
    data = loadInventoryFile()

    if origin not in data or destiny not in data:
        print("❌ Invalid 🧙 character name(s).")
        return

    originInv = data[origin]["inventory"]
    destInv = data[destiny]["inventory"]

    if itemName not in originInv:
        print(f"⚠️ 🧙 {origin} doesn't have 📦 '{itemName}'.")
        return

    if originInv[itemName]["quantity"] < quantity:
        print(f"⚠️ 🧙 {origin} doesn't have enough 📦 '{itemName}' to trade.")
        return

    # Remove from origin
    originInv[itemName]["quantity"] -= quantity
    if originInv[itemName]["quantity"] == 0:
        del originInv[itemName]

    # Add to destiny
    if itemName in destInv:
        destInv[itemName]["quantity"] += quantity
    else:
        newId = generateId(destInv)
        destInv[itemName] = {
            "id": newId,
            "quantity": quantity,
            "description": originInv.get(itemName, {}).get("description", "")
        }

    saveInventoryData(data)
    print(f"🔄 🧙 {origin} traded {quantity}x 📦 '{itemName}' to 🧙 {destiny}.")
        
def showInventory(character):
    data = loadInventoryFile()
    if character not in data:
        print(f"❌ The character 🧙 '{character}' doesn't exist.")
        return

    inventory = data[character]["inventory"]
    print(f"\n 🧙 {character}'s 🎒 inventory:")
    if not inventory:
        print("  (empty)")
        return

    for itemName, info in inventory.items():
        print(f"  - {itemName} ({info['quantity']}): {info['description']}")      

def showAllCharactersInventory():
    data = loadInventoryFile()
    if not data:
        print("❌ The party is empty!")
        return

    print("\n=== 🎒🧙 All Characters Inventories 🧙🎒 ===")
    for character, info in data.items():
        print(f"\n 🧙 {character} (ID: {info['id']}):")
        inv = info["inventory"]
        if not inv:
            print("  (empty)")
        for itemName, itemInfo in inv.items():
            print(f"  [{itemInfo['id']}] {itemName} ({itemInfo['quantity']}): {itemInfo['description']}")

def selectItem(character):
    data = loadInventoryFile()
    if character not in data:
        print(f"❌ The character 🧙 '{character}' doesn't exist.")
        return None

    inventory = data[character]["inventory"]
    if not inventory:
        print(f"⚠️ 🧙{character} has no 📦items.")
        return None

    showInventory(character)
    choice = input("Select an 📦 item (ID or name): ").strip()

    for name, info in inventory.items():
        if choice == info["id"] or choice.lower() == name.lower():
            return name

    print("❌ Invalid 📦 item selection.")
    return None      

# ===========================
#  Menus
# ===========================

def showMainMenu():
    print("\n=== MAIN MENU ===")
    print("1. Create Character ➕🧙")
    print("2. Edit Character ✏️")
    print("3. Show Character Inventory 🎒🧙")
    print("4. Show Party 🧙🤝")
    print("5. Show All Inventories 🎒🤝🧙")
    print("6. Add Item ➕📦")
    print("7. Edit Item ➕📦")
    print("8. Remove Item ➖📦")
    print("9. Trade Items 🔄")
    print("10. Delete Character ❌")
    print("11. Exit 🔹")

    option = input("Choose: ").strip()

    if option == "1":
        #Create charactere
        name = input("New 🧙 Character's name: ").strip()
        createCharacter(name)
        showInventory(name)
        showInventoryMenu(name)
    elif option == "2":
        #Edit character
        editCharacter()
    elif option == "3":
        #Show character inventory
        character = selectCharacter()
        if character:
            showInventory(character)
            showInventoryMenu(character)
    elif option == "4":
        #Show Party members
        showParty()
    elif option == "5":
        #Show all inventories
        showAllCharactersInventory()
    elif option == "6":
        #Add item
        character = selectCharacter("Add 📦 item to which 🧙 character?")
        if character:
            item = input("📦 Item's name: ").strip()
            qtd = int(input("Quantity: "))
            desc = input("Description: ").strip()
            addItem(character, item, qtd, desc)
            showInventory(character)
            showInventoryMenu(character)
    elif option == "7":
        #Edit Item
        editItem()
    elif option == "8":
        #Remove Item
        character = selectCharacter("Remove 📦 item from which 🧙 character?")
        if character:
            item = selectItem(character)
            if item:
                removeItem(character, item)
                showInventory(character)
                showInventoryMenu(character)
    elif option == "9":
        #Item Trading
        print("\n-- 🔄 Item Trade --")
        origin = selectCharacter("🧙 From (who)?")
        if origin:
            destiny = selectCharacter("🧙 To (who)?")
            if destiny:
                item = selectItem(origin)
                if item:
                    qtd = int(input("Quantity to 🔄 trade: "))
                    tradeItems(origin, destiny, item, qtd)
                    showInventory(origin)
                    showInventoryMenu(origin)
    elif option == "10":
        character = selectCharacter("Delete which 🧙 character?")
        if character:
            deleteCharacter(character)
    elif option == "11":
        global keepRunning
        keepRunning = False
        print("👋 Exiting...")
    else: 
        print("❌ Invalid option.")
        
def showInventoryMenu(character):
    print(f"\n=== {character}'s Inventory Menu 🎒🧙 ===")
    print("1. Show Other Inventory 🎒")
    print("2. Add Item ➕📦")
    print("3. Remove Item ➖📦")
    print("4. Trade Item (Me -> Other) 🔄")
    print("5. Back to Main Menu 🔹")

    option = input("Choose: ").strip()

    if option == "1":
        character = selectCharacter()
        if character:
            showInventory(character)
    elif option == "2":
        item = input("📦 Item's name: ").strip()
        qtd = int(input("Quantity: "))
        desc = input("Description: ").strip()
        addItem(character, item, qtd, desc)
    elif option == "3":
        item = selectItem(character)
        if item:
            removeItem(character, item)
    elif option == "4":
        print("\n-- 🔄 Trade Item --")
        destiny = selectCharacter("🧙 To (who)?")
        if destiny:
            item = selectItem(character)
            if item:
                qtd = int(input("Quantity to 🔄 trade: "))
                tradeItems(character, destiny, item, qtd)
    elif option == "5":
        showMainMenu()
    else:
        print("❌ Invalid option.")

if __name__ == "__main__":
    while keepRunning:
        showMainMenu()