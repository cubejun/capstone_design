<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>바코드 정보</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
    </style>
</head>
<body>

<h2>바코드 정보</h2>

<table>
    <tr>
        <th>ID</th>
        <th>바코드 데이터</th>
        <th>제품 리스트 리포트 번호</th>
        <th>제품명</th>
        <th>가격</th>
        <th>count</th>
    </tr>
    <?php
    // MySQL 데이터베이스 연결 설정
    $db_connection = mysqli_connect("localhost", "plab", "plab", "exampledb");

    // 연결 확인
    if (mysqli_connect_errno()) {
        echo "Failed to connect to MySQL: " . mysqli_connect_error();
        exit();
    }

    // 바코드 정보 쿼리
    $result = mysqli_query($db_connection, "SELECT * FROM Barcode_prototype");

    while ($row = mysqli_fetch_assoc($result)) {
        echo "<tr>";
        echo "<td>" . $row['id'] . "</td>";
        echo "<td>" . $row['barcode_data'] . "</td>";
        echo "<td>" . $row['prdlst_report_no'] . "</td>";
        echo "<td>" . $row['prdlst_nm'] . "</td>";
        echo "<td>" . $row['price'] . "</td>";
        echo "<td>" . $row['detection_count'] . "</td>";
        echo "</tr>";
    }

    // 연결 해제
    mysqli_close($db_connection);
    ?>
</table>

</body>
</html>
