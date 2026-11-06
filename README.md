# SpaceX Falcon 9 First-Stage Landing Prediction

This repository contains the final capstone project of the **IBM Data Science Professional Certificate** (course: *Applied Data Science Capstone*, IBM / Coursera).

It holds the code of the hands-on exercise notebooks completed during the capstone, the Plotly Dash application, and the final presentation. Each notebook follows one stage of a full data science workflow: collecting data, cleaning it, exploring it, building interactive visualizations, and training machine learning models.

## Project goal

SpaceX advertises Falcon 9 launches at about $62 million, while other providers charge $165 million or more. Most of the difference comes from recovering and reusing the first stage. If we can predict whether the first stage will land, we can estimate the cost of a launch. That estimate is useful to a company bidding against SpaceX.

**Question:** given a launch's site, orbit, payload mass and booster characteristics, will the first stage land successfully?

## Exercise notebooks

The notebooks are the completed IBM lab exercises, in the order they were done:

| # | Stage | File | What it does |
|---|---|---|---|
| 1 | Data collection (API) | `jupyter-labs-spacex-data-collection-api.ipynb` | Requests launch data from the SpaceX REST API, normalizes the JSON, keeps Falcon 9 launches and fills missing payload masses |
| 2 | Data collection (web scraping) | `jupyter-labs-webscraping.ipynb` | Scrapes the Falcon 9 launch tables from Wikipedia with BeautifulSoup and builds a DataFrame |
| 3 | Data wrangling | `labs-jupyter-spacex-Data_wrangling.ipynb` | Explores launch sites, orbits and landing outcomes, and creates the binary training label (landed / not landed) |
| 4 | EDA with SQL | `jupyter-labs-eda-sql-coursera_sqllite.ipynb` | Answers 10 questions about the missions with SQL queries on a SQLite database |
| 5 | EDA with visualization | `edadataviz.ipynb` | Plots relationships between flight number, payload, site, orbit and success; prepares features with one-hot encoding |
| 6 | Interactive map | `lab_jupyter_launch_site_location.ipynb` | Maps launch sites and outcomes with Folium and measures distances to the coast, roads, railways and cities |
| 7 | Dashboard | `spacex-dash-app.py` | Plotly Dash app with a site dropdown, a success pie chart and a payload-range scatter plot |
| 8 | Machine learning | `SpaceX_Machine_Learning_Prediction_Part_5.ipynb` | Trains and tunes logistic regression, SVM, decision tree and KNN with 10-fold grid search, and compares them |
| — | Presentation | `SpaceX_Capstone_Presentation.pdf` | Final report slides with methods, results and conclusions |

## Tools and libraries

- **Language and environment:** Python 3, Jupyter / JupyterLite, IBM Skills Network Labs (Cloud IDE)
- **Data collection:** `requests`, `BeautifulSoup` (bs4), REST API, JSON
- **Data handling:** `pandas`, `NumPy`
- **Databases:** SQLite, `ipython-sql` (SQL magic)
- **Visualization:** `matplotlib`, `seaborn`
- **Interactive analytics:** `Folium` (maps, marker clusters, distance lines), `Plotly` and `Dash` (dashboard)
- **Machine learning:** `scikit-learn` (`StandardScaler`, `train_test_split`, `GridSearchCV`, `LogisticRegression`, `SVC`, `DecisionTreeClassifier`, `KNeighborsClassifier`)

## Main results

- **Dataset:** 90 Falcon 9 launches between 2010 and 2020. Overall landing success rate: **66.7%**.
- **Trend:** success went from 0% (2010–2013) to 90% (2019), with a dip in 2018.
- **Launch sites:** KSC LC-39A has the highest success rate (**76.9%**, 10 of 13 launches).
- **Orbits:** GTO missions are the hardest to recover (52% over 27 flights). The 100% orbits (ES-L1, GEO, HEO, SSO) rest on only 1–5 flights each.
- **Models:**

  | Model | Cross-validation accuracy | Test accuracy |
  |---|---|---|
  | Logistic regression | 0.846 | 0.833 |
  | SVM (sigmoid kernel) | 0.848 | 0.833 |
  | Decision tree | **0.891** | 0.833 |
  | KNN (k = 10) | 0.848 | 0.833 |

  The decision tree performs best in cross-validation. On the 18-launch test set all four models get 15 of 18 right, with the same 3 false positives (failed landings predicted as successful).

## Notes and limitations

- **SpaceX API outage:** during the lab, the live `api.spacexdata.com` returned a Cloudflare 522 error (a known outage, confirmed on the course forums). The ID lookups in notebook 1 could not run, so the notebook continues from IBM's published output of the same pipeline (`dataset_part_1.csv`). The error output is kept in the notebook as a record.
- **Small test set:** with 18 test launches, one prediction changes accuracy by 5.6 points, so the four models cannot be reliably ranked.
- **Time as a hidden factor:** flight number, booster version and payload all increase over time, so the models mainly learn that later flights land more often.

## Running the dashboard

```bash
pip install pandas dash plotly
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
python spacex-dash-app.py
```

Then open http://127.0.0.1:8050 in a browser.

## Author

Argyris Livieratos, physicist. Completed as part of the IBM Data Science Professional Certificate, November 2026.

## Acknowledgements

Exercise templates, datasets and helper functions were provided by IBM Skills Network as part of the course. The completed code and analysis in these notebooks are my own work.
