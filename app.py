import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend for web-based plotting
from flask import Flask, request, render_template, send_file
import matplotlib.pyplot as plt
import numpy as np
import io

site = Flask(__name__)

@site.route('/')
def index():
    # Return the HTML template
    return render_template('index.html')

@site.route('/plot', methods=['GET'])
def plot_graph():
    # Get the temperature (T) from the URL
    T = float(request.args.get('T'))
    R = 8.3145  # in J/K.mol (using correct units)

    # Create x and y data for the graph (Avoid dividing by 0)
    vm = np.linspace(0.1, 10, 100)  # This creates an array of values between 0.1 and 10
    p = (T * R) / vm  # This calculates y = T / x for each value in x

    # Create a graph using Matplotlib
    plt.figure(figsize=(12, 8))
    plt.plot(vm, p, label=f'T = {T}')
    plt.xlabel('Volume Molar (m³/mol)')
    plt.ylabel('Pressão (Pa)')
    plt.title(f'Gráfico P x Vm')
    plt.legend()
    plt.grid()

    # Save the plot to a BytesIO object to avoid saving to disk
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')  # Save the plot in PNG format to the BytesIO object
    img_io.seek(0)  # Rewind the file-like object to the beginning
    plt.close()  # Close the plot (since we’ve saved it)

    # Return the image as a response (so the browser can show it)
    return send_file(img_io, mimetype='image/png')

# Run the Flask app
if __name__ == "__main__":
    site.run(debug=True)
