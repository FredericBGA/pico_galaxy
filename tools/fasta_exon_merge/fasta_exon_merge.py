#!/usr/bin/env python
"""Python script to combine FASTA sequence of exon entries into CDS/AA.

Example input, combines entries with suffix .1, .2, ... into single
entries.

>cds.GPLIN_000008300.t1.1
CAATGTTTCCATCGGACTTGGGGCCAAACAAATGCCTGTTGTTGATTACAAAGGCGGTTACGGATACAATAACATTGGCACATTTTGGGGTCACGAGGTCAGGGGATGTTCCCACGCCATTAATGGACGTCATTACATTTATGGAAAACCTCCGTTTGGCGTAGGCGACGTCGTCGGCTGCGGCGTTAATTTGGCAACTCGCCAAATTATTTACACAAAAAATGGGGAGCGTTTGGGTGAGAAAGAATAA
>cds.GPLIN_000008300.t1.2
AGTGGCGCGCTGTGTTCGCTGAACGGGCAATTCCAAAAGACGGCATTGTTTACTTTGAAGTAAAAGTCTTAGAACAAAAAGG
>cds.GPLIN_000008300.t1.3
GGCTAATCCCGCAACAGAATCGATGGGATTCGTCGGCTTGCCACAAAGACCTGGCGCTCTCTGAGCCCGACCGATTGATTGTCCAACATAATGGAGAGGCTAATTGGG
>cds.GPLIN_000008300.t1.4
GGAATGAATCAGCTGAAGAGAGAACTGATTGCACAGCTGCAACAGAACATTGATGCAAAGATGGAGGAGTATCAGAAGCAACAGCAACTGAACAGCGTCGACTTGCAGAAGACGGTTGCCGTGTTAAATGACACATTAAATGGAAACG
>cds.GPLIN_000008300.t1.5
TTTCCATTGATCAGTGTTCGTTGAAGCATCAGAAACACGAGAAAAAAGCTGATCAAAAAGTTCTGAGTGCAATGATTGATCAA
>cds.GPLIN_000008300.t1.6
ACCATCGACGAATTGACAGAAAAACTGAAGG
>cds.GPLIN_000008300.t1.7
GACGAATTGCATCAAATAAAAGAGGAATTGAAGAACACGAAAGAAGCTTTCGACAAAAAGCTTAAAGAACAAATG
>cds.GPLIN_000008300.t1.8
AAGCTGCTGGCGACCGGGGCAAAAATGCAGCAGAACACGGAGAAGGAAATGAATCGGCGGCTGCTAAAGAGGGGCAACAAACAAACACTGACCAATTGGAG
>cds.GPLIN_000008300.t1.9
AAGGAACTCCACGCCGAGTTGGCACATCAGAAACTGCTTAATGCTCACATGGCTCTGCAGACAAAGATGGAGGAGTATCAGAACAAAGAGCAGCAGAAGACCATCGACTCGTTGACAGAAAAACTGAAGG
>cds.GPLIN_000008300.t1.10
AACATTTGTGGCCAACTTTCACGAATTTGGACCAATCTGAAGAAGTGCGTCTTTTACGGGCCAGAAATGCTCAATTGGAACGCCAACAAACGATAAATTACGGCAAAACGTTTGAACAAATTGAACTCGAACTCGAAAAT
>cds.GPLIN_000008300.t1.11
ATGTTAATTTCGACCGAATCAACAAATGGAGGGCACATAACAACTAATCAGG
>cds.GPLIN_000008400.t1.1
ACACCGCCAATTTGTTTGTCACTTTTGCCGCCGAATTGTTCCCATGCGTTACGTTGTATAACTCTGGCGCCAAAATTGAAGCGAATTTTGGACCGAACTTTGAATACAAATTCTGA
...

Output:

>cds.GPLIN_000008300.t1 merged from 11 exons
CAATGTTTCCATCGGACTTGGGGCCAAACAAATGCCTGTTGTTGATTACAAAGGCGGTTA
CGGATACAATAACATTGGCACATTTTGGGGTCACGAGGTCAGGGGATGTTCCCACGCCAT
TAATGGACGTCATTACATTTATGGAAAACCTCCGTTTGGCGTAGGCGACGTCGTCGGCTG
CGGCGTTAATTTGGCAACTCGCCAAATTATTTACACAAAAAATGGGGAGCGTTTGGGTGA
GAAAGAATAAAGTGGCGCGCTGTGTTCGCTGAACGGGCAATTCCAAAAGACGGCATTGTT
TACTTTGAAGTAAAAGTCTTAGAACAAAAAGGGGCTAATCCCGCAACAGAATCGATGGGA
TTCGTCGGCTTGCCACAAAGACCTGGCGCTCTCTGAGCCCGACCGATTGATTGTCCAACA
TAATGGAGAGGCTAATTGGGGGAATGAATCAGCTGAAGAGAGAACTGATTGCACAGCTGC
AACAGAACATTGATGCAAAGATGGAGGAGTATCAGAAGCAACAGCAACTGAACAGCGTCG
ACTTGCAGAAGACGGTTGCCGTGTTAAATGACACATTAAATGGAAACGTTTCCATTGATC
AGTGTTCGTTGAAGCATCAGAAACACGAGAAAAAAGCTGATCAAAAAGTTCTGAGTGCAA
TGATTGATCAAACCATCGACGAATTGACAGAAAAACTGAAGGGACGAATTGCATCAAATA
AAAGAGGAATTGAAGAACACGAAAGAAGCTTTCGACAAAAAGCTTAAAGAACAAATGAAG
CTGCTGGCGACCGGGGCAAAAATGCAGCAGAACACGGAGAAGGAAATGAATCGGCGGCTG
CTAAAGAGGGGCAACAAACAAACACTGACCAATTGGAGAAGGAACTCCACGCCGAGTTGG
CACATCAGAAACTGCTTAATGCTCACATGGCTCTGCAGACAAAGATGGAGGAGTATCAGA
ACAAAGAGCAGCAGAAGACCATCGACTCGTTGACAGAAAAACTGAAGGAACATTTGTGGC
CAACTTTCACGAATTTGGACCAATCTGAAGAAGTGCGTCTTTTACGGGCCAGAAATGCTC
AATTGGAACGCCAACAAACGATAAATTACGGCAAAACGTTTGAACAAATTGAACTCGAAC
TCGAAAATATGTTAATTTCGACCGAATCAACAAATGGAGGGCACATAACAACTAATCAGG
>cds.GPLIN_000008400.t1 merged from 11 exons
ACACCGCCAATTTGTTTGTCACTTTTGCCGCCGAATTGTTCCCATGCGTTACGTTGTATA
ACTCTGGCGCCAAAATTGAAGCGAATTTTGGACCGAACTTTGAATACAAATTCTGATTAT
...

"""

import sys

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

input_fasta, output_fasta = sys.argv[1:]


def exon_merge_iter(input_records, split_on):
    """Iterate over input records spliting them into exons."""
    current_stem = None
    current_parts = []
    for record in input_records:
        stem, part = record.id.rsplit(split_on, 1)
        part = int(part)
        if stem == current_stem:
            current_parts.append(record.seq)
            assert part == len(current_parts), "Expected %s%s%i but got %s" % (
                current_stem,
                split_on,
                len(current_parts),
                record.id,
            )
        else:
            if current_parts:
                s = sum(current_parts, Seq(""))
                if len(s) % 3:
                    print(
                        "Warning %s length %i not a multiple of 3"
                        % (current_stem, len(s))
                    )
                yield SeqRecord(
                    s,
                    id=current_stem,
                    description="merged from %i exons" % len(current_parts),
                )
            current_stem = stem
            current_parts = [record.seq]
    # Final batch
    if current_parts:
        s = sum(current_parts, Seq(""))
        if len(s) % 3:
            print("Warning %s length %i not a multiple of 3" % (current_stem, len(s)))
        yield SeqRecord(
            s, id=current_stem, description="merged from %i exons" % len(current_parts)
        )


def exon_merge_files(input_filename, output_filename, split_on):
    """Do the merge, return gene count."""
    records = exon_merge_iter(SeqIO.parse(input_filename, "fasta"), split_on)
    return SeqIO.write(records, output_filename, "fasta")


count = exon_merge_files(input_fasta, output_fasta, ".")
