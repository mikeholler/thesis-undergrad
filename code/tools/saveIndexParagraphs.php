<?php

$connection = mysqli_connect('localhost', 'thesis', 'thesis', 'thesis');
if (mysqli_connect_errno()) echo mysqli_connect_error();

$result = $connection->query(
    "SELECT i.`label`, p.body
      FROM paragraph p, indexedParagraph ip, `index` i
      WHERE p.paraNum = ip.paraNum
        AND i.indexId = ip.indexId
        AND p.bookId = 1");

while ($row = $result->fetch_object()){
    $filename = str_replace("/", "_", $row->label) . '.txt';
    $filename = str_ireplace("\x0D", "", $filename);
    file_put_contents($filename, $row->body . "\n\n", FILE_APPEND);
}
