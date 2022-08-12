<h1>[CSE3330] Project Phase III</h1>
<body><p>This project focus on taking a database and creating a web
interface with a few select queries. These pages have no exception
handing or "try-catch" blocks, but instead use the queries focus on
constraints:</p>
<ol>
<li> Insert a new student in the database. Your query should insert 
values for all attributes in the PhdStudent table. Link the new 
student with an existing scholarship and also add committee 
members for the student in the PhDCommittee table.<ul> 
<li>A whole page called "Insert Student" is used to get the info of
the student using text inputs and a number input for the Semester Year</li>
<li> A query is then ran linking inserting the student in the tables
`phpStudent`,`scholarshipSupport` and `phdCommittee` a committing it to
the database</li>
</ul></li>

<li>Update the payment amount of the TAs for a course given the 
course id and updated payment amount. </li><ul>
<li>This page accept a courseID and an update to the Monthly payment by the user.
This does not do calculations from the previous month, but replace the data.</li></ul>
<li>Display Grant Title, Type, and Account No. for a GRA student.</li><ul>
<li> Similar to the insert, this has a page that accepts input of a student ID,
then uses a query to link the GRA info to the GRANT info displaying it.</li>
</ul>
<li> 
Delete a Self-Support student type who has not passed any 
milestone yet (to avoid integrity constraints). Your query 
should also reflect changes in the PhDStudent table.<ul>
<li>This has a page that will accept the student ID then use a query to delete
said student from the phdStudent table causing a cascade.</li>
</ul>
</li>
</ol>
</body>

