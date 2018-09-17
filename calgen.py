#! /usr/bin/env python3
import calendar
import sys
import os
from dateutil.easter import easter
from datetime import date, timedelta


months = ["Januar", "Februar", "Mars", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Desember"]


def generate_holydays(year):
	# Holydays with the same date every year
	holydays = {
		date(year, 1, 1): "Nyttårsdag",
		date(year, 5, 1): "Arbeidernes dag",
		date(year, 5, 17): "Grunnlovsdagen",
		date(year, 12, 25): "1. Juledag",
		date(year, 12, 26): "2. Juledag"
	}

	# Easter related stuff
	easter_sunday = easter(year)
	holydays[easter_sunday] = "1. Påskedag"
	holydays[easter_sunday + timedelta(days=1)] = "2. Påskedag"
	holydays[easter_sunday - timedelta(days=7)] = "Palmesøndag"
	holydays[easter_sunday - timedelta(days=3)] = "Skjærtorsdag"
	holydays[easter_sunday - timedelta(days=2)] = "Langfredag"
	holydays[easter_sunday + timedelta(days=39)] = "Kristi himmelfart"
	holydays[easter_sunday + timedelta(days=49)] = "1. Pinsedag"
	holydays[easter_sunday + timedelta(days=50)] = "2. Pinsedag"

	return holydays



def to_calendar_entry(date, color=None, additional_text=None):
	if color:
		add_color = "\\color{{{}}}".format(color)
	else:
		add_color = ""

	# if additional_text:
	# 	add_additional_text = "{{\\color{{gray}} \\textsuperscript{{{}}}}}".format(additional_text)
	# else:
	# 	add_additional_text = ""
	add_additional_text = ""

	if date == 0:
		return "\\cellcolor{gray!10}"
	else:
		return "\\begin{{tabular}}{{l}}{} {}. {} \\\\ \\\\ \\\\\\end{{tabular}}".format(add_color, date, add_additional_text)


def generate_calendar_tabular(year, month, holydays):
	result = ""

	cal = calendar.Calendar()

	counter=0
	for date_int in cal.itermonthdays(year, month):
		weekday = counter % 7
		if date_int != 0:
			date_obj = date(year, month, date_int)
		else:
			date_obj = None

		if weekday == 0:
			if counter != 0:
				result += "\\\\"

			result += "\\hline\n"

		else:
			result += " & "

		if date_obj in holydays:
			result += to_calendar_entry(date_int, "red", holydays[date_obj])

		elif weekday == 6:
			result += to_calendar_entry(date_int, "red")

		else:
			result += to_calendar_entry(date_int)

		counter += 1

	result += "\\\\ \\hline\n"

	pre = "\\normalsize\n\n\\begin{tabularx}{\\textwidth}{ Y  Y  Y  Y  Y  Y  Y }\n	Mandag & Tirsdag & Onsdag & Torsdag & Fredag & Lørdag & Søndag\n\\end{tabularx}\n\\small\n\\def\\arraystretch{1.5}\n\\begin{tabularx}{\\textwidth}{| X | X | X | X | X | X | X |}"
	post = "\\end{tabularx}"
	return pre + "\n" + result + "\n" + post


def generate_calandar_latex(year, month):
	calendar_file = open("{}-{}.tex".format(months[month-1], year), "w")
	pre_file = open("pre.tex", "r")
	post_file = open("post.tex", "r")

	for line in pre_file:
		calendar_file.write(line)


	calendar_file.write("\\Huge {{\\color{{gray}} {}}} \\quad {}\n".format(year, months[month-1]))
	calendar_file.write("\\vspace{30px}\n")

	holydays = generate_holydays(year)
	calendar_file.write(generate_calendar_tabular(year, month, holydays))

	for line in post_file:
		calendar_file.write(line)

	calendar_file.close()
	os.system("pdflatex {}-{}.tex > /dev/null".format(months[month-1], year))

	# Remove LaTeX junk)
	os.system("rm -f {m}-{y}.aux {m}-{y}.log {m}-{y}.synctex.gz {m}-{y}.tex".format(m=months[month-1], y=year))


if __name__ == '__main__':
	if len(sys.argv) == 3:
		generate_calandar_latex(int(sys.argv[1]), int(sys.argv[2]))

	elif len(sys.argv) == 2:
		for month in range(1, 13):
			generate_calandar_latex(int(sys.argv[1]), month)

	else:
		print("No args given. Proper use:")
		print()
		print("  > ./calgen.py year (month)")
		print()
		print("Month is optional. If omitted, calgen will make a calendar for each month in the given year")
	



