import logging
import operator
import textwrap
from reedsolo import RSCodec
from collections import defaultdict
from utils.robust_solition import PRNG
from utils.droplet import Droplet
import utils.file_process as fp
from tqdm import tqdm
logging.basicConfig(level=logging.DEBUG)
# Constants
encoded_file = '50-SF.txt'
decoded_file = '50-SF.jpg'
seed_size = 4
data_size = 16
rscode_size= 5
chunk_num = 1494
count=0
rs = RSCodec(rscode_size)
chunks = [None] * chunk_num
prng = PRNG(K=chunk_num, delta=0.05, c=0.1, np=False)
droplets = set()
done_segments = set()
chunk_to_droplets = defaultdict(set)

def droplet_recovery(dna):
    # Translating {A,C,G,T} to {0,1,2,3}
    base_mapping = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
    binary_string = ''.join(base_mapping[base] for base in dna)    
    byte_groups = [int(group, 2) for group in textwrap.wrap(binary_string, 8)]
    try:
        # Attempt to correct the substitution error with RS code
        corrected_byte_groups = rs.decode(byte_groups)[0]    
    except:
        # Exclude the sequence with error, which is founded by RS code
        return None, -1   
    # Extract Seed, data payload from the sequence
    seed_bytes = ''.join(chr(byte) for byte in corrected_byte_groups[:seed_size])
    seed = sum(ord(char) << (8 * i) for i, char in enumerate(seed_bytes[::-1]))
    data = corrected_byte_groups[seed_size:]   
    droplet = Droplet(data, seed, [])
    return droplet

def identifiers_generate(droplet):
    prng.set_seed(droplet.seed)
    droplet.num_chunks=set(prng.get_src_blocks_wrap()[1])
    droplets.add(droplet)
    for chunk_num in droplet.num_chunks:
        chunk_to_droplets[chunk_num].add(droplet)

def message_pass(droplet):
    # If the droplet contains inferred segments, XOR them, 
    # and remove them from the identity list of droplet
    for chunk_num in (droplet.num_chunks & done_segments):
        droplet.data = map(operator.xor, droplet.data, chunks[chunk_num])
        droplet.num_chunks.remove(chunk_num)
        chunk_to_droplets[chunk_num].discard(droplet)
    # If the droplet has only one segment left, 
    # set the segment to the droplet's data payload
    if len(droplet.num_chunks) == 1:
        lone_chunk = droplet.num_chunks.pop()
        chunks[lone_chunk] = droplet.data
        done_segments.add(lone_chunk)
        droplets.discard(droplet)
        chunk_to_droplets[lone_chunk].discard(droplet)
        # Recursively propagate the new inferred segment to all previous droplets 
        # until no more updates are made
        for other_droplet in chunk_to_droplets[lone_chunk].copy():
            message_pass(other_droplet)


def segment_inference(droplet):
    # Generate a list of segment identifiers
    identifiers_generate(droplet)
    # one round of message passing
    message_pass(droplet)

def decoder():
    with open(encoded_file, 'r') as f:
        for count, dna in enumerate(f, start=1):
            dna = dna.rstrip('\n')
            segment_inference(droplet_recovery(dna))
            if len(done_segments) >= chunk_num:
                break
    logging.info("After reading %d lines, we finished decoding!", count)
    outstring = ''
    logging.info("Restoring the picture now!")
    for x in tqdm(chunks):
        outstring += ''.join(map(chr, x))
    with open(decoded_file, 'wb') as f:
        f.write(outstring)
        logging.info("MD5 is %s", fp.get_md5(outstring))
    logging.info("Done!")

if __name__ == '__main__':
    decoder()

