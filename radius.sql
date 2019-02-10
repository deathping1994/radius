-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 10, 2019 at 02:33 PM
-- Server version: 5.7.25-0ubuntu0.16.04.2
-- PHP Version: 7.0.32-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `radius`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `FindNearest` (IN `_my_lat` DOUBLE, IN `_my_lon` DOUBLE, IN `_START_dist` DOUBLE, IN `_max_dist` DOUBLE, IN `_limit` INT, IN `_condition` VARCHAR(1111))  BEGIN
    
    
    
    
    
    
    

    
    DECLARE _deg2rad DOUBLE DEFAULT PI()/1800000;  

    
    
    SET @my_lat := _my_lat * 10000,
        @my_lon := _my_lon * 10000,
        @deg2dist := 0.0069172,  
        @start_deg := _start_dist / @deg2dist,  
        @max_deg := _max_dist / @deg2dist,
        @cutoff := @max_deg / SQRT(2),  
        @dlat := @start_deg,  
        @lon2lat := COS(_deg2rad * @my_lat),
        @iterations := 0;        

    
    
    
    
    
    
    SET @sql = CONCAT(
        "SELECT COUNT(*) INTO @near_ct
            FROM properties_new
            WHERE lat    BETWEEN @my_lat - @dlat
                             AND @my_lat + @dlat   -- PARTITION Pruning and bounding box
              AND lon    BETWEEN @my_lon - @dlon
                             AND @my_lon + @dlon   -- first part of PK
              AND ", _condition);
    PREPARE _sql FROM @sql;
    SELECT `debug_msg`(1, @sql) AS `debug_msg1`;
    MainLoop: LOOP
        SET @iterations := @iterations + 1;
        
        SET @dlon := ABS(@dlat / @lon2lat);  
        
        SET @dlon := IF(ABS(@my_lat) + @dlat >= 900000, 3600001, @dlon);  
        SELECT `debug_msg`(1, CONCAT_WS(",",@my_lat,@dlat,@my_lon,@dlon)) AS `parameters`;
        EXECUTE _sql;
        IF ( @near_ct >= _limit OR         
             @dlat >= @cutoff ) THEN       
            LEAVE MainLoop;
        END IF;
        
        SET @dlat := LEAST(2 * @dlat, @cutoff);   
    END LOOP MainLoop;
    DEALLOCATE PREPARE _sql;

    
    
    

    
    SET @dlat := IF( @dlat >= @max_deg OR @dlon >= 1800000,
                @max_deg,
                GCDist(ABS(@my_lat), @my_lon,
                       ABS(@my_lat) - @dlat, @my_lon - @dlon) );
            
            

    
    
    
    SET @dlon := IFNULL(ASIN(SIN(_deg2rad * @dlat) /
                             COS(_deg2rad * @my_lat))
                            / _deg2rad 
                        , 3600001);    

    
    
    IF (ABS(@my_lon) + @dlon < 1800000 OR    
        ABS(@my_lat) + @dlat <  900000) THEN 
        
        SET @sql = CONCAT(
            "SELECT *,
                    @deg2dist * GCDist(@my_lat, @my_lon, lat, lon) AS dist
                FROM properties_new
                WHERE lat BETWEEN @my_lat - @dlat
                              AND @my_lat + @dlat   -- PARTITION Pruning and bounding box
                  AND lon BETWEEN @my_lon - ABS(@dlon)
                              AND @my_lon + ABS(@dlon)   -- first part of PK
                  AND ", _condition, "
                HAVING dist <= ", _max_dist, "
                ORDER BY dist
                LIMIT ", _limit
                        );
  SELECT `debug_msg`(1, CONCAT_WS(",",@deg2dist,@my_lat,@dlat,@my_lon,@dlon)) AS `parameters`;
    ELSE
        
        
        SET @west_lon := IF(@my_lon < 0, @my_lon, @my_lon - 3600000);
        SET @east_lon := @west_lon + 3600000;
        
        SET @sql = CONCAT(
            "( SELECT *,
                    @deg2dist * GCDist(@my_lat, @west_lon, lat, lon) AS dist
                FROM properties_new
                WHERE lat BETWEEN @my_lat - @dlat
                              AND @my_lat + @dlat   -- PARTITION Pruning and bounding box
                  AND lon BETWEEN @west_lon - ABS(@dlon)
                              AND @west_lon + ABS(@dlon)  -- first part of PK
                  AND ", _condition, "
                HAVING dist <= ", _max_dist, " )
            UNION ALL
            ( SELECT *,
                    @deg2dist * GCDist(@my_lat, @east_lon, lat, lon) AS dist
                FROM properties
                WHERE lat BETWEEN @my_lat - @dlat
                              AND @my_lat + @dlat   -- PARTITION Pruning and bounding box
                  AND lon BETWEEN @east_lon - ABS(@dlon)
                              AND @east_lon + ABS(@dlon)   -- first part of PK
                  AND ", _condition, "
                HAVING dist <= ", _max_dist, " )
            ORDER BY dist
            LIMIT ", _limit
                        );
    END IF;

    PREPARE _sql FROM @sql;
    SELECT `debug_msg`(1, @sql) AS `final_sql`;

    EXECUTE _sql;
    DEALLOCATE PREPARE _sql;
END$$

--
-- Functions
--
CREATE DEFINER=`root`@`localhost` FUNCTION `debug_msg` (`enabled` INT(11), `msg` TEXT) RETURNS TEXT CHARSET latin1 READS SQL DATA
BEGIN
    IF enabled=1 THEN
    return concat('** DEBUG:', "** ", msg);
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` FUNCTION `GCDist` (`_lat1` DOUBLE, `_lon1` DOUBLE, `_lat2` DOUBLE, `_lon2` DOUBLE) RETURNS DOUBLE SQL SECURITY INVOKER
BEGIN
    
    DECLARE _deg2rad DOUBLE DEFAULT PI()/1800000;  
    DECLARE _rlat1 DOUBLE DEFAULT _deg2rad * _lat1;
    DECLARE _rlat2 DOUBLE DEFAULT _deg2rad * _lat2;
    
    DECLARE _rlond DOUBLE DEFAULT _deg2rad * (_lon1 - _lon2);
    DECLARE _m     DOUBLE DEFAULT COS(_rlat2);
    DECLARE _x     DOUBLE DEFAULT COS(_rlat1) - _m * COS(_rlond);
    DECLARE _y     DOUBLE DEFAULT               _m * SIN(_rlond);
    DECLARE _z     DOUBLE DEFAULT SIN(_rlat1) - SIN(_rlat2);
    DECLARE _n     DOUBLE DEFAULT SQRT(
                        _x * _x +
                        _y * _y +
                        _z * _z    );
    RETURN  2 * ASIN(_n / 2) / _deg2rad;   
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `properties_new`
--

CREATE TABLE `properties_new` (
  `id` int(11) NOT NULL,
  `lat` double NOT NULL,
  `lon` double NOT NULL,
  `price` double NOT NULL,
  `bath` int(11) NOT NULL,
  `bed` int(11) NOT NULL,
  `listed_on` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `requirements`
--

CREATE TABLE `requirements` (
  `id` int(11) NOT NULL,
  `lat` double NOT NULL,
  `lon` double NOT NULL,
  `max_budget` float NOT NULL,
  `min_budget` float NOT NULL,
  `min_bed` int(11) NOT NULL,
  `max_bed` int(11) NOT NULL,
  `min_bath` int(11) NOT NULL,
  `max_bath` int(11) NOT NULL,
  `listed_on` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `properties_new`
--
ALTER TABLE `properties_new`
  ADD PRIMARY KEY (`lon`,`lat`,`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD KEY `price` (`price`),
  ADD KEY `bath` (`bath`),
  ADD KEY `bed` (`bed`);

--
-- Indexes for table `requirements`
--
ALTER TABLE `requirements`
  ADD PRIMARY KEY (`lon`,`lat`,`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD KEY `max_budget` (`max_budget`),
  ADD KEY `min_budget` (`min_budget`),
  ADD KEY `min_bed` (`min_bed`),
  ADD KEY `max_bed` (`max_bed`),
  ADD KEY `max_bath` (`max_bath`),
  ADD KEY `min_bath` (`min_bath`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `properties_new`
--
ALTER TABLE `properties_new`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7636464;
--
-- AUTO_INCREMENT for table `requirements`
--
ALTER TABLE `requirements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=399467;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
