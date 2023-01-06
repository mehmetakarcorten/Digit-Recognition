import os
import tensorflow
import numpy as np
import dotenv
import shutil
import logging

tensorflow.get_logger().setLevel(logging.ERROR)


info = dotenv.find_dotenv()
dotenv.load_dotenv(info)

model_shape = eval(os.environ["MODEL_SHAPE"])
prev_model_shape = eval(os.environ["PREV_MODEL_SHAPE"])
epochs = eval(os.environ["EPOCHS"])
prev_epochs = eval(os.environ["PREV_EPOCHS"])

class Model:
	def __init__(self):
		self.activation = True
		mnist = tensorflow.keras.datasets.mnist
		(xt,yt),(xt2,yt2) = mnist.load_data()

		xt = tensorflow.keras.utils.normalize(xt,axis=1)
		xt2 = tensorflow.keras.utils.normalize(xt2,axis=1)
		if (prev_model_shape != model_shape) or (os.path.isdir("digits.model") == False) or (prev_epochs != epochs):
			try: shutil.rmtree("digits.model")
			except: pass

			model = tensorflow.keras.models.Sequential()
			model.add(tensorflow.keras.layers.Flatten(input_shape=model_shape))
			model.add(tensorflow.keras.layers.Dense(128,activation="relu"))
			model.add(tensorflow.keras.layers.Dense(128,activation="relu"))
			model.add(tensorflow.keras.layers.Dense(10,activation="softmax"))

			model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=["accuracy"])
			model.fit(xt,yt,epochs=epochs)
			model.save("digits.model")
			dotenv.set_key(info,"PREV_MODEL_SHAPE",str(model_shape))
			dotenv.set_key(info,"PREV_EPOCHS",str(epochs))

		self.model = tensorflow.keras.models.load_model("digits.model")
		self.loss, self.accuracy = self.model.evaluate(xt2,yt2)
		print(self.loss, self.accuracy)
	
	def predict(self,array):
		probabilities = {
		"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0}
		if self.activation:
			prediction = self.model.predict(array)
			for i in range(len(prediction[0])):
				probabilities[str(i)] = prediction[0][i]
			return f"This digit is probably: {np.argmax(prediction)}\n"+str(probabilities)

	def close(self):
		self.activation = False


	
