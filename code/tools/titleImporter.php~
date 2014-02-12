<?php

if (!isset($argv[1])) {
    echo 'Need to provide a title file to import.';
}

$connection = mysqli_connect(
    'localhost',
    'thesis',
    'thesis',
    'thesis'
);

/**
 * Number of titles imported for progress tracking.
 */
$count = 0;

if (mysqli_connect_errno()) {
    echo mysqli_connect_error();
}

/**
 * Helper function for mysqli_stmt_bind_param.
 */
function refValues($arr) {
	$refs = array();
	foreach ($arr as $key => $value) {
		$refs[$key] = &$arr[$key];
	}
	return $refs;
}

function insertTitles(&$titles) {
	global $connection, $count;
	$sql = 'INSERT INTO `articleTitles`'
	     . '(`title`) VALUES ';
	     
	$stmt = $connection->prepare(
	    $sql . implode(
	               ',',
	               array_fill(
	                   0, count($titles),
	                   '(?)'
	               )
	           )
	);
	
	$type = str_repeat('s', count($titles));
	
	call_user_func_array(
	    'mysqli_stmt_bind_param',
	    array_merge(
	        array($stmt, $type),
	        refValues($titles)
	    )
	);
	
	$stmt->execute();
	$count += count($titles);
	echo "$count\n";
}

// open titles file
$handle = fopen($argv[1], 'r');

$titles = array();

// Number of titles to import in one MySQL
// request. Multiple blocks of $max size
// will be imported until all titles are
// imported.
$max = 1000;

/*
 * Read a block of $max titles and insert them
 * into the database, until the dump file has
 * been completely read into the database. 
 */
while (($title = fgets($handle)) !== false) {
	$titles[] = trim($title);
	if (count($titles) == $max) {
		insertTitles($titles);
		$titles = array();
	}
}

// If count($titles) is not evenly divisible by
// $max, this last insert ensures the remainder
// of titles gets inserted into the database.
if ($titles) {
    insertTitles($titles);
}

fclose($handle);
