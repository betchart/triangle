module Triangle where

import qualified Data.Set as Set
import qualified Data.List as List

data TriBoard = TriBoard Int (Set.Set TriPoint) deriving (Show)
data TriPoint = TriPoint Int Int deriving (Show, Eq, Ord)
data TriDirection = TRight | TUpRight | TUpLeft | TLeft | TDownLeft | TDownRight
                   deriving (Eq, Ord, Show, Read, Bounded, Enum)

(!) :: TriPoint -> TriDirection -> TriPoint
(!) (TriPoint i j) direction = case direction of
                                 TRight -> TriPoint i (j+1)
                                 TUpRight -> TriPoint (i-1) j
                                 TUpLeft -> TriPoint (i-1) (j-1)
                                 TLeft -> TriPoint i (j-1)
                                 TDownLeft -> TriPoint (i+1) j
                                 TDownRight -> TriPoint (i+1) (j+1)
              
fullBoard :: Int -> TriBoard
fullBoard size = TriBoard size $ Set.fromList [TriPoint i j | i<-[0..(size-1)], j<-[0..i]]

emptyBoard :: Int -> TriBoard
emptyBoard size = TriBoard size $ Set.fromList []
                 
remove :: TriPoint -> TriBoard -> TriBoard
remove point (TriBoard size set) = TriBoard size $ Set.delete point set

move :: TriPoint -> TriPoint -> TriBoard -> TriBoard
move origin destination (TriBoard size set) = TriBoard size $
                                              Set.insert destination $
                                              Set.delete origin set
-- handle errors of origin not member, destination already filled, destination off-board?
                                              
display :: TriBoard -> String
display (TriBoard size set) = unlines [(replicate (size-i) ' ') ++
                                       (unwords [if (Set.member (TriPoint i j) set)
                                                 then "X" else "."
                                                 | j<-[0..i]])
                                       | i<-[0..(size-1)]]

neighbors :: TriPoint -> TriBoard -> [TriPoint]
neighbors p (TriBoard size set) = filter
                                  (\q -> Set.member q set)
                                  [p!d | d <- [minBound .. maxBound] :: [TriDirection]]

open :: TriPoint -> TriBoard -> Bool
open p@(TriPoint i j) (TriBoard size set) = and [0 <= j, j <= i,
                                                 0 <= i, i < size,
                                                 Set.notMember p set]

leap :: TriPoint -> TriDirection -> TriBoard -> TriBoard
leap p d board = let leaped = p!d in 
                 remove leaped $ move p (leaped!d) board

leaps :: TriPoint -> TriBoard -> [TriDirection]
leaps p board@(TriBoard size set) = filter (\d -> (Set.member (p!d) set) &&
                                                  (open (p!d!d) board)
                                           ) [minBound..maxBound] :: [TriDirection]

triSolutions :: TriBoard -> [[TriBoard]]
triSolutions board@(TriBoard size set) = case Set.size set of
                                           1 -> [[board]]
                                           otherwise ->  map (\t -> board:t) $ concat
                                                         [triSolutions (leap p d board) |
                                                          p <- (Set.toList set),
                                                          d <- (leaps p board)]
