<?php
// goal was to get a random line from file, and save it, so we can fetch it later in js, or something like this, I think  

$target_dir = "../../dice/data/";
$target_file = $target_dir . basename("list.txt");

// I feel like I'm doing something dumb, perhaps one day I'll look at this and fix it
$array = json_encode(explode("\r\n",file_get_contents($target_file))); // transform file to json
file_put_contents($target_dir."mbs.txt",$_REQUEST["name"].": ".json_decode($array)[array_rand(json_decode($array))]); // and save random element from it(? what am I doing)

?>
