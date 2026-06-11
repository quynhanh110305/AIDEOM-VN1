# AIDEOM-VN Dashboard

Web app Streamlit tích hợp 12 bài tập mô hình ra quyết định phát triển kinh tế Việt Nam.

## Chạy local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy lên Streamlit Cloud

1. Tạo repo GitHub, push toàn bộ thư mục này lên.
2. Vào https://share.streamlit.io → **New app** → chọn repo → file `app.py`.
3. Click **Deploy** — xong trong ~2 phút.

## Nội dung 12 bài

| Module | Kỹ thuật |
|---|---|
| Bài 1 – Cobb-Douglas & TFP | Numpy, phân rã tăng trưởng |
| Bài 2 – LP Ngân sách | scipy.linprog, shadow price |
| Bài 3 – Priority Index | MCDM, Min-Max norm |
| Bài 4 – LP Vùng miền | PuLP 6×4, ràng buộc công bằng |
| Bài 5 – MIP Dự án | Binary selection, tiên quyết |
| Bài 6 – TOPSIS | Entropy weights, sensitivity |
| Bài 7 – Pareto | Monte Carlo, biên Pareto |
| Bài 8 – Tối ưu động | SLSQP, quỹ đạo 2026-2035 |
| Bài 9 – Lao động AI | LP NetJob, 8 ngành |
| Bài 10 – Stochastic LP | 2-stage, VSS, EVPI |
| Bài 11 – Q-Learning | Tabular RL, 81 trạng thái |
| Bài 12 – Dashboard | 5 kịch bản, KPI tổng hợp |

## Dữ liệu
Dữ liệu Việt Nam 2020-2025 nhúng trực tiếp trong `app.py` (GSO/NSO, World Bank, MoST).
