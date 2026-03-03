import requests

# === ВАШИ ДАННЫЕ ===
ORG_ID = "ID_ВАШЕЙ_ОРГАНИЗАЦИИ"
TOKEN = "ВАШ_OAUTH_ТОКЕН"
TARGET_EMAIL = "nickname@domain.ru" # Почта для пересылки

# Базовые настройки API
URL = f"https://api360.yandex.net/admin/v1/org/{ORG_ID}/mail/routing/rules"
HEADERS = {
    "Authorization": f"OAuth {TOKEN}",
    "Content-Type": "application/json"
}

# Полный список расширений, которые нужно заблокировать/переслать
EXTENSIONS = [
    "ade", "adp", "apk", "app", "appx", "asp", "appxbundle", "bas", "bat", "bin", "cab", "chm",
    "cla", "class", "cmd", "cnt", "com", "cpl", "crt", "csh", "dll", "dmg", "drv", "ex", "ex_",
    "exe", "fxp", "gadget", "grp", "hlp", "hpj", "hta", "inf", "ink", "ins", "isp", "iso", "its",
    "jar", "js", "jse", "ksh", "lib", "lnk", "mad", "maf", "mag", "mam", "maq", "mar", "mas",
    "mat", "mau", "mav", "maw", "mcf", "mda", "mdb", "mde", "mdt", "mdw", "mdz", "msc", "msh",
    "mshxml", "msh1", "msh1xml", "msh2", "msh2xml", "msi", "msix", "msixbundle", "msp", "mst",
    "nlm", "nsh", "ocx", "ops", "osd", "ovl", "pcd", "pif", "pl", "plg", "prf", "prg", "ps1",
    "ps1xml", "ps2", "ps2xml", "psc1", "psc2", "pst", "reg", "rtf", "scf", "scr", "sct", "sh",
    "shb", "shs", "sys", "vb", "vba", "vbe", "vbp", "vbs", "vhd", "vsmacros", "vsw", "vxd", "ws",
    "wsc", "wsf", "wsh", "xbap", "xnk"
]

def main():
    print("1. Получение текущих правил...")
    get_response = requests.get(URL, headers=HEADERS)
    
    if get_response.status_code != 200:
        print(f"Ошибка при получении правил: {get_response.status_code}\n{get_response.text}")
        return

    # Извлекаем массив текущих правил (если правил нет, создаем пустой список)
    current_data = get_response.json()
    rules = current_data.get("rules", [])
    print(f"   Найдено текущих правил: {len(rules)}")

    print("2. Генерация нового правила с расширениями...")
    # Программно создаем список условий "$or" для каждого расширения
    conditions = [{"attach:filename": {"$contains": f".{ext}"}} for ext in EXTENSIONS]

    new_rule = {
        "terminal": False,
        "condition": {
            "$or": conditions
        },
        "actions": [
            {
                "action": "forward",
                "data": {
                    "email": TARGET_EMAIL
                }
            }
        ],
        "scope": {
            "direction": "inbound"
        }
    }

    print("3. Добавление нового правила в список...")
    rules.append(new_rule)
    
    # Формируем итоговый JSON-объект для отправки
    payload = {"rules": rules}

    print("4. Отправка обновленных правил на сервер...")
    put_response = requests.put(URL, headers=HEADERS, json=payload)

    if put_response.status_code == 200:
        print("✅ Успех! Новое правило успешно добавлено, старые сохранены.")
    else:
        print(f"❌ Ошибка при сохранении: {put_response.status_code}\n{put_response.text}")

if __name__ == "__main__":
    main()