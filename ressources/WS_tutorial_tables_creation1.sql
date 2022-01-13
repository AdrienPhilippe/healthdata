-- phpMyAdmin SQL Dump
-- version 4.6.6deb4+deb9u2
-- https://www.phpmyadmin.net/
--
-- Client :  localhost:3306
-- Généré le :  Lun 23 Novembre 2020 à 14:31
-- Version du serveur :  10.1.47-MariaDB-0+deb9u1
-- Version de PHP :  7.0.33-0+deb9u10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------

--
-- Structure de la table `messages`
--

DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages` (
  `dest` varchar(50) NOT NULL,
  `text` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `messages`
--

INSERT INTO `messages` (`dest`, `text`) VALUES
('all', 'Hello world !'),
('birds', 'Hello birds !'),
('boys', 'Hello boys !'),
('cats', 'Hello cats !'),
('dogs', 'Hello dogs !'),
('ducks', 'Hello ducks !'),
('girls', 'Hello girls !'),
('men', 'Hello men !'),
('women', 'Hello women !');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `idUser` int(11) NOT NULL,
  `loginUser` varchar(50) NOT NULL,
  `pwdUser` varchar(50) NOT NULL,
  `rights` enum('read','all','') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `users`
--

INSERT INTO `users` (`idUser`, `loginUser`, `pwdUser`, `rights`) VALUES
(1, 'Joan', '*C4B90000B75BB7AAB97655238B97325CDB66F96A', 'read'),
(2, 'Mary', '*3A23E1093E954158272BD54EFCE2E8EC01356EB0', 'all');

--
-- Index pour les tables exportées
--

--
-- Index pour la table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`dest`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`idUser`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `idUser` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

COMMIT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
