import Triangle

main = do
  putStrLn $ unlines $ map display $ head $ triSolutions $ remove (TriPoint 0 0) $ fullBoard 6
