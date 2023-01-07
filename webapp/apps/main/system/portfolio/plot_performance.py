import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_performance(data):
	# Plot three charts: Equity curve,
	# period returns, drawdowns
	fig = plt.figure()
	# Set the outer colour to white
	fig.patch.set_facecolor('white')
	# Plot the equity curve
	ax1 = fig.add_subplot(311, ylabel='Portfolio value, %')
	data['equity_curve'].plot(ax=ax1, color="blue", lw=2.)
	plt.grid(True)
	# Plot the returns

	ax2 = fig.add_subplot(312, ylabel='Period returns, %')
	data['returns'].plot(ax=ax2, color="black", lw=2.)
	plt.grid(True)
	# Plot the returns
	ax3 = fig.add_subplot(313, ylabel='Drawdowns, %')
	data['drawdown'].plot(ax=ax3, color="red", lw=2.)
	plt.grid(True)
	# Plot the figure
	plt.tight_layout()
	plt.show()

# TODO: draw heatmap for sharpe ratio, etc...
def create_data_matrix(csv_ref, col_index):
	data = np.zeros((3, 3))
	for i in range(0, 3):
		for j in range(0, 3):
			data[i][j] = float(csv_ref[i*3+j][col_index])
	return data
