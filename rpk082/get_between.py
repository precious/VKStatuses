def get_between(data, initial, first, last):
	if data.find(first) == -1 or data.find(last) == -1:
		return None
	begin = data.find(first, initial) + len(first)
	end = data.find(last, begin)
	return data[begin:end]
