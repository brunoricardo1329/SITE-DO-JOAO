<?php
$config = array(
    'user' => 'root',
    'password' => 'B1dCBBa-2Bf4d5Bhhfe6AGaf1E24hCFA',
    'host' => 'roundhouse.proxy.rlwy.net',
    'port' => 19533,
    'database' => 'railway'
);

$mysqli = new mysqli($config['host'], $config['user'], $config['password'], '', $config['port']);

if ($mysqli->connect_error) {
    die("Connection failed: " . $mysqli->connect_error);
}

$createDatabaseQuery = "CREATE DATABASE IF NOT EXISTS " . $config['database'];
if ($mysqli->query($createDatabaseQuery) === TRUE) {
    echo "Database created successfully or already exists.\n";
} else {
    echo "Error creating database: " . $mysqli->error;
    $mysqli->close();
    exit();
}

$mysqli->select_db($config['database']);

$createTableQuery = "CREATE TABLE IF NOT EXISTS tabela (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operator VARCHAR(255) NOT NULL,
    machineType VARCHAR(255) NOT NULL,
    repairDate DATE NOT NULL,
    repairTime DATETIME NOT NULL,
    repairer VARCHAR(255) NOT NULL
)";
if ($mysqli->query($createTableQuery) === TRUE) {
    echo "Table created successfully or already exists.\n";
} else {
    echo "Error creating table: " . $mysqli->error;
    $mysqli->close();
    exit();
}

$data = json_decode(file_get_contents('php://input'), true);

$insertQuery = "INSERT INTO tabela (operator, machineType, repairDate, repairTime, repairer) VALUES (?, ?, ?, ?, ?)";
$stmt = $mysqli->prepare($insertQuery);
$stmt->bind_param('sssss', $data['operator'], $data['machineType'], $data['repairDate'], $data['repairTime'], $data['repairer']);

if ($stmt->execute()) {
    echo json_encode(['success' => true]);
} else {
    echo json_encode(['error' => 'Failed to insert data.']);
}

$stmt->close();
$mysqli->close();
?>
