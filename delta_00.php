<?php 
include("header.php"); 
?>
<script type="text/javascript" src="dist/jquery.tabledit.js"></script>

<div class="container home">		 
	<table id="data_table" class="table table-striped">
		<thead>
			<tr>
				<th>date</th>
                                <th>altitude</th>
                                <th>azimuth</th>
				<th>alb_rad</th>
				<th>asob_s</th>
				<th>aswdifd_s</th>	
				<th>aswdifu_s</th>
				<th>aswdir_s</th>
				<th>cape_con</th>
				<th>clc</th>
				<th>clch</th>	
				<th>clcl</th>
				<th>clcm</th>
				<th>clct</th>
				<th>clct_mod</th>
				<th>hbas_con</th>
				<th>mh</th>
                                <th>omega</th>
                                <th>p</th>
                                <th>qv</th>	
				<th>qv_2m</th>
				<th>qv_s</th>
				<th>rain_con</th>
				<th>rain_gsp</th>
                                <th>relhum</th>
				<th>relhum_2m</th>
				<th>snow_con</th>	
				<th>snow_gsp</th>
                                <th>t</th>
				<th>t_2m</th>
                                <th>tke</tke>
				<th>tmax_2m</th>
				<th>tmin_2m</th>
                                <th>u</th>
                                <th>v</th>
                                <th>w</th>	
				<th>power_calc</th>
				<th>power_real</th>
				<th>power_error</th>
                                <th>power_correct</th>	
			</tr>
		</thead>
		<tbody>
			<?php 
                        $db_connection=pg_connect("host=localhost dbname=test user=user1 password=123456");
			$resultset = pg_query($db_connection, "SELECT * FROM forecast_delta_00 ORDER BY date DESC") or die("database error:". pg_error($db_connection));
			while( $developer = pg_fetch_assoc($resultset) ) {
			?>
			   <tr id="<?php echo $developer ['date']; ?>">
			   <td><?php echo $developer ['date']; ?></td>
			   <td><?php echo $developer ['altitude']; ?></td>
			   <td><?php echo $developer ['azimuth']; ?></td>
			   <td><?php echo $developer ['alb_rad']; ?></td>
			   <td><?php echo $developer ['asob_s']; ?></td>
			   <td><?php echo $developer ['aswdifd_s']; ?></td>   
			   <td><?php echo $developer ['aswdifu_s']; ?></td>
			   <td><?php echo $developer ['aswdir_s']; ?></td>   
			   <td><?php echo $developer ['cape_con']; ?></td>
			   <td><?php echo $developer ['clc']; ?></td>
			   <td><?php echo $developer ['clch']; ?></td>
			   <td><?php echo $developer ['clcl']; ?></td>
			   <td><?php echo $developer ['clcm']; ?></td>   
			   <td><?php echo $developer ['clct']; ?></td>
			   <td><?php echo $developer ['clct_mod']; ?></td>   
			   <td><?php echo $developer ['hbas_con']; ?></td>
			   <td><?php echo $developer ['mh']; ?></td>
			   <td><?php echo $developer ['omega']; ?></td>
			   <td><?php echo $developer ['p']; ?></td>   
			   <td><?php echo $developer ['qv']; ?></td>
			   <td><?php echo $developer ['qv_2m']; ?></td>   
			   <td><?php echo $developer ['qv_s']; ?></td>
			   <td><?php echo $developer ['rain_con']; ?></td>
			   <td><?php echo $developer ['rain_gsp']; ?></td>
			   <td><?php echo $developer ['relhum']; ?></td>   
			   <td><?php echo $developer ['relhum_2m']; ?></td>
			   <td><?php echo $developer ['snow_con']; ?></td>   
			   <td><?php echo $developer ['snow_gsp']; ?></td>
			   <td><?php echo $developer ['t']; ?></td>
			   <td><?php echo $developer ['t_2m']; ?></td>
			   <td><?php echo $developer ['tke']; ?></td>   
			   <td><?php echo $developer ['tmax_2m']; ?></td>
			   <td><?php echo $developer ['tmin_2m']; ?></td>  
	                   <td><?php echo $developer ['u']; ?></td>   
			   <td><?php echo $developer ['v']; ?></td>
			   <td><?php echo $developer ['w']; ?></td>    
	                   <td><?php echo $developer ['power_calc']; ?></td>   
			   <td><?php echo $developer ['power_real']; ?></td>
			   <td><?php echo $developer ['power_error']; ?></td>   
			   <td><?php echo $developer ['power_correct']; ?></td>   
			   </tr>
			<?php } ?>
		</tbody>
    </table>	

</div>
<script type="text/javascript" src="custom_table_edit.js"></script>

 



                                                                                                       
