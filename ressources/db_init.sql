CREATE TABLE `Patients` (
  `id_patient` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL DEFAULT 'None',
  `firstname` text NOT NULL DEFAULT 'None',
  `email` text NOT NULL UNIQUE DEFAULT 'None',
  `password` text NOT NULL DEFAULT 'None',
  `birthdate` text NOT NULL DEFAULT 'None',
  `sex` text NOT NULL DEFAULT 'None',
  `age` INT NOT NULL DEFAULT 0,
  `height` INT NOT NULL DEFAULT 0
);

CREATE TABLE `Doctors` (
  `id_doctor` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL DEFAULT 'None',
  `firstname` text NOT NULL DEFAULT 'None',
  `email` text NOT NULL UNIQUE DEFAULT 'None',
  `password` text NOT NULL DEFAULT 'None'
);

CREATE TABLE `Relations` (
  `id_doctor` INT NOT NULL,
  `id_patient` INT NOT NULL,
  FOREIGN KEY (id_doctor) REFERENCES Doctors(id_doctor),
  FOREIGN KEY (id_patient) REFERENCES Patients(id_patient)
);

CREATE TABLE `Datas` (
  `id_data` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `id_patient` INT NOT NULL DEFAULT 0,
  `timestamp` text NOT NULL DEFAULT '0',
  `weight` INT NOT NULL DEFAULT 0,
  `chest` INT NOT NULL DEFAULT 0,
  `abdomen` INT NOT NULL DEFAULT 0,
  `hip` INT NOT NULL DEFAULT 0,
  `heartbeat` INT NOT NULL DEFAULT 0,
  FOREIGN KEY (id_patient) REFERENCES Patients(id_patient)
);

CREATE TABLE `Messages` (
  `id_message` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `timestamp` text NOT NULL DEFAULT '0',
  `id_patient` INT NOT NULL,
  `id_doctor` INT NOT NULL,
  `body` text NOT NULL DEFAULT '',
  FOREIGN KEY (id_doctor) REFERENCES Doctors(id_doctor),
  FOREIGN KEY (id_patient) REFERENCES Patients(id_patient)
)