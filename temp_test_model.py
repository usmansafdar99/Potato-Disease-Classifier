import tensorflow as tf
from pathlib import Path
p = Path('d:/Potato/1')
print('path exists', p.exists(), p)
try:
    m = tf.keras.models.load_model(str(p))
    print('keras load type', type(m))
except Exception as e:
    print('keras load failed:', type(e), e)
    try:
        m2 = tf.saved_model.load(str(p))
        print('saved model load type', type(m2))
        print('has summary', hasattr(m2, 'summary'))
        if hasattr(m2, 'summary'):
            try:
                m2.summary()
                print('summary worked')
            except Exception as e2:
                print('summary failed:', type(e2), e2)
    except Exception as e3:
        print('saved model failure:', type(e3), e3)
