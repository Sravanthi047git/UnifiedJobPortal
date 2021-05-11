from dice_final import scrape_dice
from glassdoor_final import scrape_glassdoor
from indeed_final import scrape_indeed
import sys

# Take input from the user
ip = int(input("Press 1 for dice extract, 2 for indeed, 3 for glassdoor, 4 for all...."))

#ip = int(sys.argv[4])

# Take job designation and location as input parameters and pass to the corresponding script
job_desig = input("Enter the job designation you are interested in: ")
#job_desig = str(sys.argv[1])

job_loc = input("Enter the job location you are interested in: ")
#job_loc = str(sys.argv[2])

no_of_jobs = int(input("How many jobs you want to scrape? "))
#no_of_jobs = int(sys.argv[3])

print("reformat the parameters as per Indeed")
in_pos = job_desig.replace(" ", "+")
in_loc = job_loc.replace(" ", "+")

if ip == 1:
    print("Scrapping data from Dice")
    scrape_dice(job_desig, job_loc, no_of_jobs)

elif ip == 2:
    print("Scrapping data from Indeed")
    scrape_indeed(in_pos, in_loc, no_of_jobs)

elif ip == 3:
    print("Scrapping data from Glassdor")
    scrape_glassdoor(job_desig, job_loc, no_of_jobs)

elif ip == 4:
    print("Scrapping data from Dice")
    scrape_dice(job_desig, job_loc, no_of_jobs)

    print("Scrapping data from Indeed")
    scrape_indeed(in_pos, in_loc, no_of_jobs)

    print("Scrapping data from Glassdor")
    scrape_glassdoor(job_desig, job_loc, no_of_jobs)

else:
    print("Entered number is not in the choice...!")
