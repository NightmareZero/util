package main

import (
	"github.com/urfave/cli"
	"os"
	"strconv"
	"time"
)

var (
	app      *cli.App
	mode     RUN_MODE // run mode
	seconds  = true   // use milliseconds
	str_date = false  // yyyy-MM-dd
	input    = ""     // user input value
	input2   = ""
)

const (
	TS RUN_MODE = 1 // time to str
	ST RUN_MODE = 2 // str to time
)

type RUN_MODE int8

func main() {
	setCmd()
	if err := app.Run(os.Args); err != nil {
		println("err", err)
	}
	if outputMode() {
		println("======== starting ========")
		doSomething()
	}

}

func setCmd() {
	app = cli.NewApp()
	app.Name = "TimeConvertor"
	app.Version = "0.0.1"
	app.Flags = []cli.Flag{
		cli.BoolFlag{
			Name:        "second, s",
			Usage:       "time use second, default milliseconds",
			Destination: &seconds,
		},
		cli.BoolFlag{
			Name:        "date, d",
			Usage:       "str with date only yyyy-MM-dd, dafault datetime yyyy-MM-dd hh:mm:ss",
			Destination: &str_date,
		},
	}
	app.Commands = []cli.Command{
		{
			Name:    "time",
			Usage:   "trans long time to str",
			Aliases: []string{"t"},
			Action: func(c *cli.Context) {
				mode = TS
				input = c.Args().First()
			},
		},
		{
			Name:    "str",
			Usage:   "trans str to long time",
			Aliases: []string{"s"},
			Action: func(c *cli.Context) {
				mode = ST
				input = c.Args().Get(0)
				input2 = c.Args().Get(1)
			},
		},
	}

}

func outputMode() bool {
	if mode != TS && mode != ST {
		return false
	}

	if !seconds {
		println("time format:", "milliseconds")
	} else {
		println("time format:", "seconds")
	}

	if str_date {
		println("str format:", "yyyy-MM-dd")
	} else {
		println("str format:", "yyyy-MM-dd hh:mm:ss")
	}

	if mode == TS {
		println("run mode:", "time to str")
	} else if mode == ST {
		println("run mode:", "str to time")
	} else {
		println("run mode:", "error")
		println("please use help command")
	}

	return true
}

func doSomething() {
	if mode == TS {
		transTimeToStr()
	}
	if mode == ST {
		transStrToTime()
	}
}

func transTimeToStr() {
	atoi, err := strconv.Atoi(input)
	var itTime time.Time
	if nil != err {
		println("err input val format")
	}
	if seconds {
		itTime = time.Unix(int64(atoi), 0)
	} else {
		itTime = time.Unix(0, int64(atoi*1000000))
	}
	itTime = itTime.Add(-8 * time.Hour)
	if str_date {
		println(itTime.Format("2006-01-02"))
	} else {
		println(itTime.Format("2006-01-02 15:04:05"))
	}
}

func transStrToTime() {
	var parse time.Time
	var err error
	if str_date {
		parse, err = time.Parse("2006-01-02", input)
	} else {
		parse, err = time.Parse("2006-01-02 15:04:05", input+" "+input2)
	}
	parse = parse.Add(-8 * time.Hour)
	if err != nil {
		println("error input val format")
		println(err)
		return
	}
	if !seconds {
		println(parse.UnixNano() / 1000000)
	} else {
		println(parse.Unix())
	}
}
