<!DOCTYPE HTML>
<?php
	$saveErrors = null;
	$paraId = null;
	$p = array();
	$p['bookId'] = isset($_POST['bookId']) ? $_POST['bookId'] : '';
	// $p['paraNum'] = isset($_POST['paraNum']) ? $_POST['paraNum'] : '';
	$p['pageNum'] = isset($_POST['pageNum']) ? $_POST['pageNum'] : '';
	$p['endPageNum'] = (isset($_POST['endPageNum']) and $_POST['endPageNum']) ? $_POST['endPageNum'] : $p['pageNum'];
	$p['entries'] = (isset($_POST['entries']) and $_POST['entries']) ? explode(';', $_POST['entries']) : '';
	$p['body'] = isset($_POST['body']) ? $_POST['body'] : '';

	if ($_SERVER['REQUEST_METHOD'] == 'POST') {
		$conn = mysqli_connect('localhost', 'thesis', 'thesis', 'thesis');
		if (mysqli_connect_errno()) $saveErrors = mysqli_connect_error();
		else {
			$stmt = $conn->prepare('INSERT INTO paragraph (`bookId`, `pageNum`, `endPageNum`, `body`) VALUES (?,?,?,?)');
			$stmt->bind_param('iiis', $p['bookId'], $p['pageNum'], $p['endPageNum'], $p['body']);
			$stmt->execute();
			$paraId = $stmt->insert_id;
			if ($stmt->affected_rows == -1) $saveErrors = $stmt->error;
		}

		if (!$saveErrors) {
			foreach ($p['entries'] as $entry) {
				$entry = trim($entry);
				echo "Entry: $entry\n";
				$sql = "SELECT `indexId` FROM `index` WHERE BINARY `label` = '" . $conn->real_escape_string($entry) . "'";
				$result = $conn->query($sql);
				echo mysqli_connect_error();
				if (!$result or !$result->num_rows) {
					$saveErrors = "No entry found with value $entry.";
					break;
				} else {
					if($row = $result->fetch_assoc()) {
						$result->free();
						$stmt = $conn->prepare('INSERT INTO indexedParagraph (`indexId`, `paraNum`) VALUES (?, ?)');
						$stmt->bind_param('ii', $row['indexId'], $paraId);
						$stmt->execute();
					} else {
						$result->free();
						$saveErrors = "No entry found with vaule $entry. 2";
					}
				}
			}
		}

	}
?>
<html>
	<head>
		<script>
			function inc(e, n) {
				textBox = document.getElementById(e);
				textBox.value = parseInt(textBox.value) + n;
			}
		</script>
	</head>
	<body>
		<h1>Paragraph Enterer</h1>
		<form method="post">
			Book ID: <input type="text" name="bookId" value="<?php echo $p['bookId'];?>"><br />
			Start Page: <input type="text" name="pageNum" id="pageNum" size="5" value="<?php echo $p['pageNum'];?>">
				<button type="button" onclick="inc('pageNum', -1)">v</button>
				<button type="button" value="^" onclick="inc('pageNum', 1)">^</button><br />
			End Page: <input type="text" name="endPageNum" id="endPageNum" size="5" value="<?php echo $p['endPageNum'];?>">
				<button type="button" onclick="inc('endPageNum', -1)">v</button>
				<button type="button" value="^" onclick="inc('endPageNum', 1)">^</button><br />
			Entries: <input type="text" name="entries" value=""><br />
			Body: <br />
			<textarea name="body" rows="10" cols="80"><?php if ($saveErrors) echo $p['body']; ?></textarea><br />
			<input type="submit">
		</form>
		<?php
			if ($_SERVER['REQUEST_METHOD'] == 'POST') {
				if ($saveErrors) echo "PROBLEM SAVING PARAGRAPH: <pre>$saveErrors</pre>";
				else echo "Saved paragraph for book {$p['bookId']}.";
			}
		?>
	</body>
</html>
