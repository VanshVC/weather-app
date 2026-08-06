# ⛅ Skylight Weather App

A premium, modern, light-themed weather dashboard built using **Python**, **Streamlit**, and the **OpenWeatherMap API**. Features a clean layout, interactive unit toggles, and full mobile responsiveness.

---

## 🌟 Features

- **Outfit Typography**: Uses a modern sans-serif typeface imported from Google Fonts for a clean aesthetic.
- **FontAwesome Vectors**: Employs colored vector icons for meteorological metrics (Feels Like, Humidity, Wind Speed, Cloud Cover, Pressure, and Visibility).
- **Responsive Layout**: 
  - Main weather card and metrics automatically wrap based on screen dimensions.
  - The **5-Day Forecast** adapts dynamically: displays as a 5-column horizontal grid on desktop/tablets, and transforms into a structured vertical rows list on mobile view.
- **Unit Conversion**: Easily toggle between Metric (`°C` and `m/s`) and Imperial (`°F` and `mph`) systems.
- **Local Astronomy Times**: Computes local sunrise and sunset times adjusted specifically to the timezone offset of the queried location.
- **Robust Layout**: Prevents screen overflows and wrapping glitches on smaller viewports.

---

## 🚀 Installation & Setup

1. **Clone or Download the Project**:
   Ensure you place the folder structure in your workspace.

2. **Set Up a Virtual Environment** (Optional but recommended):
   ```bash
   # Create a virtualenv
   python -m venv myenv
   
   # Activate it (Windows)
   myenv\Scripts\activate
   
   # Activate it (Mac/Linux)
   source myenv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API Key**:
   Create a file named `.env` in the root directory and add your OpenWeatherMap API key:
   ```env
   API_KEY=your_openweathermap_api_key_here
   ```

---

## 💻 Running the App

Start the Streamlit development server locally:
```bash
streamlit run app.py
```

Open `http://localhost:8501` (or the port specified in the terminal) in your web browser.
