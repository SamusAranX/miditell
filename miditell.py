#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from glob import glob
from os.path import join, exists, basename, realpath, split, splitext
from sys import exit

import midi

# reset working dir after importing because sf2_loader fucks with it for no good reason
real_cwd = os.getcwd()
import sf2_loader as sf2
os.chdir(real_cwd)


def get_sf2_instruments(path):
	sf2_file = sf2.sf2_loader(path)

	instruments = {}
	for b in range(128):
		instruments[b] = {}
		for i in range(128):
			inst_name = sf2_file.get_instrument_name(bank_num=b, preset_num=i)
			if not inst_name:
				if i == 0:
					# probably found an empty bank. abort
					break

				continue

			instruments[b][i] = inst_name

	return instruments


def get_sf2_for_midi(midi_path):
	midi_dir, midi_file = split(midi_path)
	midi_dir_base = basename(midi_dir)
	midi_base, _ = splitext(midi_file)

	base_sf2 = join(midi_dir, f"{midi_base}.sf2")
	dir_sf2 = join(midi_dir, f"{midi_dir_base}.sf2")

	if exists(base_sf2):
		return base_sf2
	elif exists(dir_sf2):
		return dir_sf2
	else:
		loose_sf2s = glob(join(midi_dir, "*.sf2"))
		if len(loose_sf2s) == 1:
			return loose_sf2s[0]

	return None


def main(args):
	if not args.soundfont:
		args.soundfont = get_sf2_for_midi(args.input)

	if not args.soundfont:
		print("please specify a soundfont!")
		exit(1)

	all_instruments = get_sf2_instruments(args.soundfont)
	found_instruments = set()

	pattern = midi.read_midifile(args.input)
	bank_idx = 0
	for track in pattern:
		for event in track:
			if event.statusmsg == 0xB0:  # control change
				if event.data[0] == 0:  # Bank MSB
					bank_idx = event.data[1]

			if event.statusmsg == 0xC0:  # program change
				inst_idx = event.data[0]
				found_instruments.add((bank_idx, inst_idx))

	for bank, inst in sorted(list(found_instruments)):
		inst_name = all_instruments[bank][inst]
		print(f"{bank:>3} - {inst:>3}: {inst_name}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="miditell")
	parser.add_argument("-i", "--input", metavar="input", type=realpath, required=True, help="midi file")
	parser.add_argument("-s", "--soundfont", metavar="soundfont", type=str, help="sf2 file (autodetected if not specified)")
	main(parser.parse_args())
