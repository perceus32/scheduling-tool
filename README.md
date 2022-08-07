## scheduling-tool

# Fetching and Cleaning Data
1. Read each company csv data into a list
2. Changed the column name to make it uniform.
3. Merged multiple companies data into a single one. Deleted duplicate entries.
4. Added NaN
5. Added PR (priority values).
6. Sort in the descending order of Priority.
7. Reset index.

# Algo

1. Created the slots to be filled using possible_combinations looping over ALL the timeslots and panel numbers. last(third) element is 0 by default for 'unassigned'.
2. Created column for company_slot and panel number.

-iterate through the candidates i.e. the rows.
-then take one company at a time.
-if the candidate is shortlisted, do for the company or lite.
-take possible combinations for that company.
-if timeslot taken, skip the iteration 
-else for a given timeslot find a free panel
-assign panel and timeslot
-change the status of the timeslot-panel pair as assigned ie. [x,y,1] so that that panel and ts is not iterated again.
-add the pair-list to non-iter so that it gets skipped for the next student 
-break out of the nested loop since pair alloted to the student 
-continue with the same student and next company
-
