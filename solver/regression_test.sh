for f in test_sketches/*
do
  echo $f 
  python3 solver.py $f
done
