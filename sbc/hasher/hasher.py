
def chunk(in_string, num_chunks):
	chunk_size = len(in_string) // num_chunks
	if len(in_string) % num_chunks: chunk_size += 1
	iterator = iter(in_string)
	for _ in range(num_chunks):
		accumulator = list()
		for _ in range(chunk_size):
			try:
				accumulator.append(next(iterator))
			except StopIteration:
				break
		yield ''.join(accumulator)


class SymbolTable:  # absolute useless shit
	def get_symbol_by_ord(num) -> int:
		return chr(num)

	def get_order_by_symbol(symbol) -> str:
		return ord(symbol)