from utility.plot_manager import PlotManager

multi_polar_path = ["./static/real_s21.csv", \
    "./static/wifi_s21_chart.csv"]
share_subplot_path = ["./static/real_s21.csv", \
    "./static/wifi_s21_chart.csv", \
    "./static/real_s21.csv", \
    "./static/wifi_s21_chart.csv"]

if __name__ == "__main__":

  PlotManager.Scatter("./static/real_s21.csv")
  PlotManager.MultiScatter(multi_polar_path)
  PlotManager.ShareScatter(share_subplot_path)

  PlotManager.Polar("./static/real_s21.csv")
  PlotManager.MultiPolar(multi_polar_path)
  PlotManager.SharePolar(share_subplot_path)

  PlotManager.Bar("./static/real_s21.csv")
  PlotManager.ShareBar(share_subplot_path)

  PlotManager.Show()
