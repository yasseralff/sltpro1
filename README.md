---

# Technical Documentation — **Sigra** (Sign Language Recognition Assistant)

---

## 1. General Project Information

** Project Purpose:**  
Sigra — это веб-приложение на базе Streamlit, предназначенное для распознавания американского языка жестов (ASL) по загруженному изображению или фото с камеры. Система использует **Google Gemini API** для интерпретации жестов и отображает ответы в удобном чат-интерфейсе.

---

### Key Functionalities:

-  **Загрузка изображений** или фотографирование через камеру.
-  **Автоматическое распознавание ASL-буквы** с помощью Google Gemini.
-  **Проверка на наличие лица** — защита конфиденциальности.
-  **Режим тренировки жестов** — интерактивная практика ASL-букв с обратной связью и баллами.
-  **Генерация ответа в формате**: `The detected letter is {letter}`.
-  Интерактивный чат-интерфейс с сохранением истории сообщений.

---

### Architecture Overview

- **Front-end:**  
  Streamlit Web UI  
  - Загрузка изображений  
  - Работа с камерой  
  - Отображение распознанных букв  
  - Управление режимами

- **Back-end:**  
  Google Gemini (via `google.generativeai`)  
  - Обработка изображений  
  - Генерация текста на основе ASL изображений

- **Дополнительно:**  
  Используются OpenCV + PIL + MediaPipe для:
  - Детекции лица  
  - Предобработки изображений  
  - Обрезки области с рукой (опционально)

---

## 2. Project Setup and Execution

### Установка:

```bash
git clone https://github.com/username/sigra.git
cd sigra
pip install -r requirements.txt
```

### Настройка API:

Создайте `.streamlit/secrets.toml`:

```toml
[secrets]
api_key = "your-gemini-api-key"
```

### Запуск проекта:

```bash
streamlit run app.py
```

---

## 3. Error Troubleshooting

### Наиболее частые ошибки:

| Ошибка | Решение |
|-------|---------|
| `ModuleNotFoundError` | Установите недостающую библиотеку через `pip install` |
| `AttributeError: 'NoneType' object has no attribute 'read'` | Убедитесь, что файл действительно загружен перед обработкой |
| `Face detected in image` | Используйте фото без лица — повторно загрузите или обрежьте изображение |
| `Gemini error` | Проверьте API-ключ и поддерживаемый формат изображения |

### Отладка:

- Используйте `st.error`, `st.warning`, `st.write()` для логирования шагов.
- Проверяйте логику `uploaded_file`, `camera_input` и `image_to_use`.

---

## 4. External Libraries and Tools

Установите через `pip`:

```bash
pip install streamlit google-generativeai opencv-python pillow mediapipe
```

Используемые библиотеки:

- `Streamlit` — интерфейс
- `Google Generative AI` — обработка изображений
- `OpenCV` — обработка изображений, распознавание лиц
- `PIL` — загрузка и конвертация изображений
- `MediaPipe` — распознавание жестов (опционально)

---

## 5. Limitations and Future Improvements

### Ограничения:

- Обрабатываются только отдельные ASL-буквы (без фраз).
- Нужен стабильный интернет.
- Gemini может ошибаться при плохом освещении или некачественном изображении.

### Планы по улучшению:

-  Добавить поддержку **ASL-фраз** (Hello, My name is...).
-  Улучшить **обрезку рук** с помощью MediaPipe + OpenCV.
-  Интерактивный **режим обучения с прогрессом**.
-  Интеграция с **Telegram-ботом** или **email уведомлениями**.
-  Добавить поддержку видео (ASL анимации).
-  Обучить собственный модель. 

---

### Структура проекта:

```
/sigra
├── app.py                # Основной интерфейс Streamlit
├── function.py           # Генерация ответов Gemini + предобработка
├── requirements.txt
├── images                # Файл с каждым жестом буквы ASL алфавита 
└── .streamlit/secrets.toml
```

---
* **Documentation**:

  * [Streamlit](https://6igsm0ke-sltpro1-gemini-app-adik-zrhf5p.streamlit.app/)
  

Sigra — создано с целью обучения, инклюзивности и повышения доступности жестового языка через AI.
