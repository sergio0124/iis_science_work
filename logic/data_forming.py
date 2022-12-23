import base64
from io import BytesIO
from matplotlib.figure import Figure


def get_image(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    image = base64.b64encode(buf.getbuffer()).decode("ascii")
    return image
