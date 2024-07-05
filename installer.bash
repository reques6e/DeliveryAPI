#!/bin/bash

# Функция для установки dialog
install_dialog() {
  if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y dialog
  elif command -v yum &> /dev/null; then
    sudo yum install -y dialog
  elif command -v dnf &> /dev/null; then
    sudo dnf install -y dialog
  elif command -v zypper &> /dev/null; then
    sudo zypper install -y dialog
  else
    echo "Не удалось определить пакетный менеджер. Установите 'dialog' вручную."
    exit 1
  fi
}

# Проверка наличия dialog, установка при необходимости
if ! command -v dialog &> /dev/null; then
  echo "Утилита 'dialog' не найдена. Установка..."
  install_dialog
fi

# Проверка наличия файла LICENSE
if [[ ! -f "LICENSE" ]]; then
  echo "Файл LICENSE не найден!"
  exit 1
fi

# Вывод содержимого файла LICENSE
dialog --title "Лицензионное соглашение" --textbox LICENSE 20 60

# Спрашиваем согласие
dialog --yesno "Согласны ли вы с условиями лицензии?" 10 60
response=$?

# Проверка ответа пользователя
if [ $response -ne 0 ]; then
  dialog --msgbox "Вы не согласились с условиями лицензии." 10 60
  clear
  exit 0
fi

# Меню выбора пункта
choices=$(dialog --menu "Пожалуйста, выберите пункт:" 15 50 3 \
1 "тест 1" \
2 "тест 2" \
3 "тест 3" 3>&1 1>&2 2>&3)

clear

case $choices in
  1)
    echo "Вы выбрали 'тест 1'"
    ;;
  2)
    echo "Вы выбрали 'тест 2'"
    ;;
  3)
    echo "Вы выбрали 'тест 3'"
    ;;
  *)
    echo "Неверный выбор"
    ;;
esac
