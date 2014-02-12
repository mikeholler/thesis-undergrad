<?php

function unwikify($title) {
    return str_replace('_', ' ', $title);
}

if (!isset($argv[1])) {
    echo 'Need to provide a intersect file to import.';
    exit(1);
}

$connection = mysqli_connect('localhost', 'thesis', 'thesis', 'thesis');

if (mysqli_connect_errno()) echo mysqli_connect_error();

$intersectionSql = 'INSERT INTO indexToWiki (indexTitle, wikiTitle) VALUES (?,?)';

// open intersection file
$handle = fopen($argv[1], 'r');

while (($wikiTitle = fgets($handle)) !== false) {
    $wikiTitle = trim($wikiTitle);
    $indexTitle = unwikify($wikiTitle);

    $stmt = $connection->prepare($intersectionSql);
    $stmt->bind_param('ss', $indexTitle, $wikiTitle);
    $stmt->execute();

    if (mysqli_errno($connection)) {echo mysqli_error($connection); exit;}

    echo "$wikiTitle\n";
}

fclose($handle);
