def generate_subnet_from_supernet(ip, cidr_supernet, cidr_subnet):
	# :param ip : <str> an IP address that fits within the given supernet
	# :param cidr_supernet : <str> bits marked for masking the supernet
	# :param cidr_subnet : <str> bits marked for masking the subnet
    results = []
	# find the network address of the given ip, as it pertains to the supernet
    binary_base = ip_to_binary(ip_to_network(ip, cidr_supernet))
	# isolate the high-order bits from the working bits of the function operation
    high_order = binary_base[:int(cidr_supernet)]
	# determine the length of working bits to loop
    relevant_bits_length = int(cidr_subnet) - int(cidr_supernet)
    # 2 to the power of relevant bits
    for x in range(2**relevant_bits_length):
        relevant_bits = bin(x).split('b')[1]
		# append zeroes until string meets length of relevant bits
        while len(relevant_bits) < relevant_bits_length:
            relevant_bits = '0' + relevant_bits
		# append relevant bits to high order bits
        unit = high_order + relevant_bits
		# append zeroes to high-order bits until 32-bit
        while len(unit) < 32:
            unit += '0'
        results.append(binary_to_ip(unit))
    return results


# return network address of a given IP address and CIDR bits
def ip_to_network(ip, cidr):
	# :param ip : <str>
	# :param cidr : <str> number, not containing slash, representing set high-order bits
	# convert IP address to a 32-bit binary string
    ip_binary = ip_to_binary(ip)
	# convert CIDR number to 32-bit binary string
    cidr_binary = cidr_to_binary(cidr)
	# logical AND of the two binary strings after converting to integer
    net_dword = int(ip_binary, 2) & int(cidr_binary, 2)
    net_binary = bin(net_dword).split('b')[1]
	# append zeroes to high-order bits until 32-bit
    while len(net_binary) < 32:
        net_binary = '0' + net_binary
	# split binary string into four octets then convert to dotted-decimal notation
    network_id = '{0}.{1}.{2}.{3}'.format(
        int(net_binary[:8], 2),
        int(net_binary[8:16], 2),
        int(net_binary[16:24], 2),
        int(net_binary[24:32], 2),
    )
    return network_id


#  return 32-bit binary string of a given IP address
def ip_to_binary(ip):
	# split dotted-decimal notation into one variable per octet
    o1, o2, o3, o4 = ip.split('.')
	# instantiate a blank string to store results
    binary = ''
    for octet in [o1, o2, o3, o4]:
		# temporarily store the binary representation of a given octet
        tmp_octet = bin(int(octet)).split('b')[1]
		# prepend zeroes to low-order bits until 8-bit
        while len(tmp_octet) < 8:
            tmp_octet = '0' + tmp_octet
		# append converted octet to results string
        binary += tmp_octet
    return binary


# return IP address of a given 32-bit binary string
def binary_to_ip(binary):
	# split binary string into four octets then convert to dotted-decimal notation
    ip = '{0}.{1}.{2}.{3}'.format(
        int(binary[:8], 2),
        int(binary[8:16], 2),
        int(binary[16:24], 2),
        int(binary[24:32], 2),
    )
    return ip


# return 32-bit binary string containing number of high-order bits set as per CIDR number
def cidr_to_binary(cidr):
    binary = ''
	# append a set bit to a string according to a given CIDR number
    for x in range(int(cidr)):
        binary += '1'
	# until 32-bit, append remaining low-order bits with zeroes
    while len(binary) < 32:
        binary += '0'
    return binary


# example function providing all /22 networks of a given /8 network address that 3.59.12.47 fits inside
print generate_subnet_from_supernet('3.59.12.47','8','22')