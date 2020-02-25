<?php
$db_connection=pg_connect("host=localhost dbname=test user=user1 password=123456");
$input = filter_input_array(INPUT_POST);
$b=$_GET['id'];
if ($input['action'] == 'edit') {	
	$update_field='';
	if(isset($input['power_calc'])) {
		$update_field.= "power_calc='".$input['power_calc']."'";
	} else if(isset($input['power_real'])) {
		$update_field.= "power_real='".$input['power_real']."'";
	} else if(isset($input['power_error'])) {
		$update_field.= "power_error='".$input['power_error']."'";
	} else if(isset($input['power_correct'])) {
		$update_field.= "power_correct='".$input['power_correct']."'";
	} else if(isset($input['designation'])) {
		$update_field.= "designation='".$input['designation']."'";
	}	

        $dt=$input['date'];



        if($b=="ao_00.php")
	if($update_field && $input['date']) {		
			$resultset = pg_query($db_connection, "UPDATE forecast_omao_00 SET $update_field WHERE date='" . $input['date'] . "'") or die("database error:". pg_error($db_connection));
   	 $resultset = pg_query($db_connection, "SELECT power_calc,power_real FROM forecast_omao_00 WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
$row=pg_fetch_row($resultset);
if(isset($row[0])&&isset($row[1]))
{
$er=$row[0]-$row[1];
$resultset = pg_query($db_connection, "UPDATE forecast_omao_00 SET power_error='" . $er . "' WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
}
	}


      if($b=="ao_06.php")
	if($update_field && $input['date']) {		
			$resultset = pg_query($db_connection, "UPDATE forecast_omao_06 SET $update_field WHERE date='" . $input['date'] . "'") or die("database error:". pg_error($db_connection));
   	 $resultset = pg_query($db_connection, "SELECT power_calc,power_real FROM forecast_omao_06 WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
$row=pg_fetch_row($resultset);
if(isset($row[0])&&isset($row[1]))
{
$er=$row[0]-$row[1];
$resultset = pg_query($db_connection, "UPDATE forecast_omao_06 SET power_error='" . $er . "' WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
}
	}

      if($b=="ao_12.php")
	if($update_field && $input['date']) {		
			$resultset = pg_query($db_connection, "UPDATE forecast_omao_12 SET $update_field WHERE date='" . $input['date'] . "'") or die("database error:". pg_error($db_connection));
   	 $resultset = pg_query($db_connection, "SELECT power_calc,power_real FROM forecast_omao_12 WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
$row=pg_fetch_row($resultset);
if(isset($row[0])&&isset($row[1]))
{
$er=$row[0]-$row[1];
$resultset = pg_query($db_connection, "UPDATE forecast_omao_12 SET power_error='" . $er . "' WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
}
	}

        if($b=="iy_00.php")
	if($update_field && $input['date']) {		
			$resultset = pg_query($db_connection, "UPDATE forecast_ospriy SET $update_field WHERE date='" . $input['date'] . "'") or die("database error:". pg_error($db_connection));
   	 $resultset = pg_query($db_connection, "SELECT power_calc,power_real FROM forecast_ospriy WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
$row=pg_fetch_row($resultset);
if(isset($row[0])&&isset($row[1]))
{
$er=$row[0]-$row[1];
$resultset = pg_query($db_connection, "UPDATE forecast_ospriy SET power_error='" . $er . "' WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
}
	}

        if($b=="iy_06.php")
	if($update_field && $input['date']) {		
			$resultset = pg_query($db_connection, "UPDATE forecast_ospriy_06 SET $update_field WHERE date='" . $input['date'] . "'") or die("database error:". pg_error($db_connection));
   	 $resultset = pg_query($db_connection, "SELECT power_calc,power_real FROM forecast_ospriy_06 WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
$row=pg_fetch_row($resultset);
if(isset($row[0])&&isset($row[1]))
{
$er=$row[0]-$row[1];
$resultset = pg_query($db_connection, "UPDATE forecast_ospriy_06 SET power_error='" . $er . "' WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
}
	}

        if($b=="iy_12.php")
	if($update_field && $input['date']) {		
			$resultset = pg_query($db_connection, "UPDATE forecast_ospriy_12 SET $update_field WHERE date='" . $input['date'] . "'") or die("database error:". pg_error($db_connection));
   	 $resultset = pg_query($db_connection, "SELECT power_calc,power_real FROM forecast_ospriy_12 WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
$row=pg_fetch_row($resultset);
if(isset($row[0])&&isset($row[1]))
{
$er=$row[0]-$row[1];
$resultset = pg_query($db_connection, "UPDATE forecast_ospriy_12 SET power_error='" . $er . "' WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
}
	}

        if($b=="ul_00.php")
	if($update_field && $input['date']) {		
			$resultset = pg_query($db_connection, "UPDATE forecast_oul_00 SET $update_field WHERE date='" . $input['date'] . "'") or die("database error:". pg_error($db_connection));
   	 $resultset = pg_query($db_connection, "SELECT power_calc,power_real FROM forecast_oul_00 WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
$row=pg_fetch_row($resultset);
if(isset($row[0])&&isset($row[1]))
{
$er=$row[0]-$row[1];
$resultset = pg_query($db_connection, "UPDATE forecast_oul_00 SET power_error='" . $er . "' WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
}
	}


        if($b=="ul_06.php")
	if($update_field && $input['date']) {		
			$resultset = pg_query($db_connection, "UPDATE forecast_oul_06 SET $update_field WHERE date='" . $input['date'] . "'") or die("database error:". pg_error($db_connection));
   	 $resultset = pg_query($db_connection, "SELECT power_calc,power_real FROM forecast_oul_06 WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
$row=pg_fetch_row($resultset);
if(isset($row[0])&&isset($row[1]))
{
$er=$row[0]-$row[1];
$resultset = pg_query($db_connection, "UPDATE forecast_oul_06 SET power_error='" . $er . "' WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
}
	}

        if($b=="ul_12.php")
	if($update_field && $input['date']) {		
			$resultset = pg_query($db_connection, "UPDATE forecast_oul_12 SET $update_field WHERE date='" . $input['date'] . "'") or die("database error:". pg_error($db_connection));
   	 $resultset = pg_query($db_connection, "SELECT power_calc,power_real FROM forecast_oul_12 WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
$row=pg_fetch_row($resultset);
if(isset($row[0])&&isset($row[1]))
{
$er=$row[0]-$row[1];
$resultset = pg_query($db_connection, "UPDATE forecast_oul_12 SET power_error='" . $er . "' WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
}
	}
        if($b=="ta_00.php")
	if($update_field && $input['date']) {		
			$resultset = pg_query($db_connection, "UPDATE forecast_delta_00 SET $update_field WHERE date='" . $input['date'] . "'") or die("database error:". pg_error($db_connection));
   	 $resultset = pg_query($db_connection, "SELECT power_calc,power_real FROM forecast_delta_00 WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
$row=pg_fetch_row($resultset);
if(isset($row[0])&&isset($row[1]))
{
$er=$row[0]-$row[1];
$resultset = pg_query($db_connection, "UPDATE forecast_delta_00 SET power_error='" . $er . "' WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
}
	}


        if($b=="ta_06.php")
	if($update_field && $input['date']) {		
			$resultset = pg_query($db_connection, "UPDATE forecast_delta_06 SET $update_field WHERE date='" . $input['date'] . "'") or die("database error:". pg_error($db_connection));
   	 $resultset = pg_query($db_connection, "SELECT power_calc,power_real FROM forecast_delta_06 WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
$row=pg_fetch_row($resultset);
if(isset($row[0])&&isset($row[1]))
{
$er=$row[0]-$row[1];
$resultset = pg_query($db_connection, "UPDATE forecast_delta_06 SET power_error='" . $er . "' WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
}
	}
        if($b=="ta_12.php")
	if($update_field && $input['date']) {		
			$resultset = pg_query($db_connection, "UPDATE forecast_delta_12 SET $update_field WHERE date='" . $input['date'] . "'") or die("database error:". pg_error($db_connection));
   	 $resultset = pg_query($db_connection, "SELECT power_calc,power_real FROM forecast_delta_12 WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
$row=pg_fetch_row($resultset);
if(isset($row[0])&&isset($row[1]))
{
$er=$row[0]-$row[1];
$resultset = pg_query($db_connection, "UPDATE forecast_delta_12 SET power_error='" . $er . "' WHERE date='" . $dt . "'") or die("database error:". pg_error($db_connection));
}
	}


}


