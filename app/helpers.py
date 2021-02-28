
def split(arr, n):
	return [arr[i * n:(i + 1) * n] for i in range((len(arr) + n - 1) // n)]


def objs_by_key(arr, key):
	return {i[key]: i for i in arr}


def retry(func):
	def call_retry(*args):
		for try_ in range(5):
			try:
				return func(*args)
			except Exception as e:
				print('Got error:', e)
	return call_retry

