# UI customization guide

Use this when you have 60-90 minutes and want the app to look sharper without rebuilding the whole thing.

## where the frontend lives

- `app.py` controls the Streamlit layout, sections, sliders, metrics, and charts.
- `styles.css` controls the custom visual styling.
- `.streamlit/config.toml` controls Streamlit's theme colors.

## easiest upgrade path

1. Open `styles.css`.
2. Change the colors in the `:root` block.
3. Tweak `.hero`, `[data-testid="stMetric"]`, and `.block-container`.
4. Refresh the Streamlit page.

## using the tools you mentioned

### lovable

Use it for ideas, not as the final source of truth. Prompt it like this:

```text
make a clean robotics predictive maintenance dashboard.
show a hero section, four model metric cards, a feature importance chart,
sensor sliders, and a prediction panel. keep it practical and technical.
```

Then copy useful wording/layout ideas into `app.py`, or copy CSS ideas into `styles.css`.

### 21st.dev

Good for component inspiration. Look for dashboard cards, metric cards, and data panels. If it gives React/Tailwind code, translate the design idea into Streamlit:

- React card -> `st.container()` or a custom CSS block
- Tailwind colors -> `styles.css` variables
- dashboard grid -> `st.columns(...)`

### reactbits.dev

Good for motion ideas, but do not spend too long here. Streamlit is not React, so copy the concept, not the code. Good targets:

- subtle animated header
- hover effect inspiration
- clean section spacing

Put CSS-only ideas in `styles.css`.

### ui.glass/generator

Use this for the hero or metric cards. Copy the generated CSS into `styles.css`, usually under:

```css
.hero {
  /* paste glass styles here */
}
```

or:

```css
[data-testid="stMetric"] {
  /* paste card styles here */
}
```

Keep readability first. If the text gets hard to read, lower blur/transparency.

### motionsites.ai

Use this for visual direction and layout rhythm. Do not try to port a whole motion site into Streamlit tonight. Steal:

- spacing
- section order
- color pairing
- button/card treatment

### glowui.com/icons

Streamlit does not have a normal icon component system like React. Use icons lightly in text labels, or skip them for speed. For GitHub, a clean technical dashboard beats icon hunting.

## high-impact changes for tonight

- make the hero title cleaner
- make the metric cards look intentional
- add one screenshot to the README
- change chart colors in `show_feature_importance()` inside `app.py`
- add a short project explanation section under the prediction area

## where to insert common changes

### change the top hero text

Edit `show_header()` in `app.py`.

### change metric card style

Edit `[data-testid="stMetric"]` in `styles.css`.

### change page width

Edit `.block-container` in `styles.css`.

### change chart colors

Edit this line inside `show_feature_importance()` in `app.py`:

```python
ax.barh(result.feature_importance["feature"], result.feature_importance["importance"])
```

Try:

```python
ax.barh(result.feature_importance["feature"], result.feature_importance["importance"], color="#0f766e")
```

## don't do tonight

- do not rebuild in React unless you are dropping the Python ML demo
- do not add auth
- do not add a database
- do not spend more than 20 minutes picking colors
- do not fight custom animations
