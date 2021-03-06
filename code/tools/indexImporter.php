<?php

if (!isset($argv[1])) {
    echo 'Need to provide a index file to import.';
    exit(1);
}

if (!isset($argv[2])) {
    echo 'Need to provide a book id';
    exit (2);
}

echo "\n$argv[1]\n";
echo "$argv[2]\n";

$connection = mysqli_connect(
    'localhost',
    'thesis',
    'thesis',
    'thesis'
);

if (mysqli_connect_errno()) {
    echo mysqli_connect_error();
    exit(1);
}

// open intersect file
$handle = fopen($argv[1], 'r');

$indexSql = 'INSERT INTO `index`'
          . '(`bookId`, `label`, `wikiLabel`)'
          . 'VALUES (?, ?, ?)';
$indexType = 'iss';

$indexedPageSql = 'INSERT INTO `indexedPage`'
                . '(`indexId`, `pageNum`)'
                . 'VALUES (?, ?)';
$indexedPageType = 'is';

while (($entry = fgets($handle)) !== false) {
    $pieces = explode(', ', $entry);
    $wikiLabel = str_replace($pieces[0], ' ', '_');

    echo $pieces[0];

    // Insert entry into index table.
    $indexStmt = $connection->prepare($indexSql);
    
    if (mysqli_errno($connection)) {
        echo mysqli_error($connection);
        exit
    }
    
    $indexStmt->bind_param(
        $indexType,
        $argv[2],
        $pieces[0],
        $wikiLabel
    );
    
    $indexStmt->execute();
    
    if (mysqli_errno($connection)) {
        echo mysqli_error($connection);
        exit;
    }
    
    $id = $indexStmt->insert_id;
    echo "|$id|";
    $indexStmt->close();


    // Insert each individual index page location.
    for ($i = 1; $i < count($pieces); $i++) {

        $indexedPageStmt = $connection->prepare(
            $indexedPageSql
        );

        $indexedPageStmt->bind_param(
            $indexedPageType,
            $id,
            $pieces[$i]
        );
        
        $indexedPageStmt->execute();
        
        if (mysqli_errno($connection)) {
            echo mysqli_error($connection);
            exit;
        }
        
        $indexedPageStmt->close();
        echo '.';
    }

    echo "\n";
}

fclose($handle);
